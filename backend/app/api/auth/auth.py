"""
File: app/api/auth/auth.py

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
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_token,
)
from app.schemas.auth import AuthResponse, TokenData, UserCreate, RefreshUser

import logging

req_logger = logging.getLogger("app_requests")
flow_logger = logging.getLogger("app_flow")
security_logger = logging.getLogger("security_logger")
db_logger = logging.getLogger("app_db")

router = APIRouter(prefix="/auth", tags=["auth"])
# router = APIRouter()

def validate_password(password: str):
    flow_logger.info("in validate_password")
    if len(password) < 8:
        raise HTTPException(400, "Password must be >= 8 characters")
    # Add checks for uppercase, numbers, etc.


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
    req_logger.info("Register request received")
    try:
        db_logger.info("checking if user exists")
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
    validate_password(form_data.password)
    user_doc = {
        "username": form_data.username,
        "hashed_password": get_password_hash(form_data.password),
    }
    try:
        db_logger.info("saving user")
        res = await users_col(db).insert_one(user_doc)
        db_logger.info("fetching user")
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
    req_logger.info("Login request received")
    db_logger.info("fetching user")
    user = await users_col(db).find_one(
        {"username": form_data.username}, 
        projection={"hashed_password": 1, "username": 1}
    )
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        flow_logger.error(
            "Failed login attempt for username: %s (IP: %s)",
            form_data.username,
            # request.client.host
            # TODO: implement this to add IP address of client. gets complicated if using reverse proxy
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid creds",
            headers={"WWW-Authenticate": "Bearer"},
        )

    tok_data = TokenData(username=user["username"])
    access_token = create_access_token(tok_data)
    refresh_token = create_refresh_token(tok_data)
    
    db_logger.info("saving refresh token")
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


@router.post(
    "/refresh", 
    response_model=AuthResponse,
    status_code=status.HTTP_202_ACCEPTED
)
async def refresh(
    form_data: RefreshUser,
):
    flow_logger.info("in refresh")
    req_logger.info("refresh request received")
    try:
        username = verify_token(form_data.refresh_token, token_type=form_data.token_type)
    except Exception as e:
        flow_logger.error("Error verifying refresh token: %s", str(e))
        raise e
    
    token_data = TokenData(username=username)
    new_access_token = create_access_token(token_data)

    return AuthResponse(
        username=username,
        access_token=new_access_token,
        refresh_token=form_data.refresh_token,
        token_type="Bearer"
    )
