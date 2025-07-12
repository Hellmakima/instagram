"""
### File: app/api/auth/auth.py

Contains the authentication related endpoints
"""
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from motor.motor_asyncio import AsyncIOMotorDatabase
from app.db.db import get_db
from app.db.collections import users_col, refresh_tokens_col

from app.core.config import settings
from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_token,
)
from app.schemas.auth import AuthResponse, TokenData, UserCreate, RefreshUser, LogoutRequest
from app.models.user import UserCreate as UserCreateModel

import logging

flow_logger = logging.getLogger("app_flow")
security_logger = logging.getLogger("security_logger")

router = APIRouter(prefix="/auth", tags=["auth"])
# router = APIRouter()


@router.post(
    "/register",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED
)
async def register(
    form_data: UserCreate,
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    flow_logger.info("in register")
    try:
        if await users_col(db).find_one({"username": form_data.username}):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User exists"
            )
    except HTTPException as e:
        flow_logger.error("Error HTTPException: %s", str(e))
        # Re-raise any HTTPExceptions coz User already exists
        raise e
    except Exception as e:
        flow_logger.error("Error checking user existence: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error checking user"
        )

    try:
        user_doc = await UserCreateModel(
            username=form_data.username,
            password=form_data.password
        ).doc()
    except Exception as e:
        flow_logger.error("Error creating user model: %s", str(e))
        raise e

    try:
        res = await users_col(db).insert_one(user_doc)
        rec = await users_col(db).find_one({"_id": res.inserted_id})
    except Exception as e:
        flow_logger.error("Error saving user to DB: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error saving user"
        )
    if not rec:
        flow_logger.error("Error fetching user from DB")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching user"
        )
    tok_data = TokenData(username=rec["username"])
    access_token = create_access_token(tok_data)
    refresh_token = create_refresh_token(tok_data)

    security_logger.info("User %s registered", rec["username"])
    
    return AuthResponse(
        username=rec["username"],
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="Bearer",
    )


@router.post(
    "/login", 
    response_model=AuthResponse,
    status_code=status.HTTP_202_ACCEPTED
)
async def login(
    # request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    flow_logger.info("in login")
    user = await users_col(db).find_one(
        {"username": form_data.username}, 
        projection={"hashed_password": 1, "username": 1}
    )
    if not user or not await verify_password(form_data.password, user["hashed_password"]):
        flow_logger.error(
            "Failed login attempt for username: %s (IP: %s)",
            form_data.username,
            "localhost"
            # request.client.host
            # TODO: implement this to add IP address of client. gets complicated if using reverse proxy
        )
        security_logger.warning(
            "Failed login attempt for username: %s (IP: %s)",
            form_data.username,
            "localhost"
            # request.client.host
            # TODO: implement this to add IP address of client. gets complicated if using reverse proxy
        )
        print("here")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    tok_data = TokenData(username=user["username"])
    access_token = create_access_token(tok_data)
    refresh_token = create_refresh_token(tok_data)
    
    # TODO: this is not completely implemented, handle revoked tokens.
    await refresh_tokens_col(db).insert_one({
        "user_id": user["_id"],
        "refresh_token": refresh_token,
        "expires_at": datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES),
        "revoked": False
    })
    
    security_logger.info("User %s logged in", user["username"])
    
    return AuthResponse(
        username=user["username"],
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="Bearer",
    )

from app.core.csrf import CsrfProtect
from fastapi import Request
from fastapi.responses import JSONResponse
@router.post(
    "/refresh", 
    response_model=AuthResponse,
    status_code=status.HTTP_202_ACCEPTED
)
async def refresh(
    form_data: RefreshUser,
    request: Request,
    csrf_protect: CsrfProtect = Depends(),
):
    await csrf_protect.validate_csrf(request)    # <-- make sure token matches

    flow_logger.info("in refresh")
    try:
        username = verify_token(form_data.refresh_token, token_type=form_data.token_type)
    except Exception as e:
        flow_logger.error("Error verifying refresh token: %s", str(e))
        raise e
    
    token_data = TokenData(username=username)
    new_access_token = create_access_token(token_data)

    # TODO: optionally rotate the refresh token
    # TODO: add a check to see if the user is blocked

    return AuthResponse(
        username=username,
        access_token=new_access_token,
        refresh_token=form_data.refresh_token,
        token_type="Bearer"
    )
    # optional: unset csrf cookie. do this for important endpoints only (e.g., logout, password change)
    # resp = JSONResponse(content=response.dict())
    # csrf_protect.unset_csrf_cookie(resp)
    # return resp


@router.post("/logout")
async def logout(
    form_data: LogoutRequest,
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    # TODO: redo this endpoint. manage token blacklisting with expiry time.
    """
    Logout endpoint
    deletes refresh token from DB
    """
    flow_logger.info("in logout")
    try:
        await refresh_tokens_col(db).delete_one({"refresh_token": form_data.refresh_token})
    except Exception as e:
        flow_logger.error("Error deleting refresh token: %s", str(e))
        raise e
    