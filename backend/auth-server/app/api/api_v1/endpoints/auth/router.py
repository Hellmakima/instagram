# auth-server/app/api/api_v1/endpoints/auth/router.py
# Contains /register, /login, /logout, /refresh_token

from fastapi import APIRouter, Cookie, Depends, HTTPException, Request, Response, status
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_token,
)
from app.schemas.auth import (
    SuccessMessageResponse,
    TokenData,
    UserCreate,
    RefreshUser,
    LogoutRequest,
    ErrorDetail,
    APIErrorResponse,
)
from app.models.user import UserCreate as UserCreateModel
from app.core.csrf import CsrfProtect, csrf_exception_handler
from fastapi_csrf_protect.exceptions import CsrfProtectError
from fastapi.templating import Jinja2Templates

from motor.motor_asyncio import AsyncIOMotorDatabase
from app.db.db import get_db
from app.db.collections import users_col, refresh_tokens_col

import logging
flow_logger = logging.getLogger("app_flow")
security_logger = logging.getLogger("security_logger")

router = APIRouter()

# TODO: fix it's place. (decide which file to put it)
@router.get(
        "/csrf-token", 
        response_class=JSONResponse
)
async def generate_csrf_token(
    csrf_protect: CsrfProtect = Depends(),
):
    csrf_token, signed_token = csrf_protect.get_csrf_token()
    response = JSONResponse(
        status_code=200,
        content={"csrf_token": csrf_token}
    )
    csrf_protect.set_csrf_cookie(signed_token, response)
    return response


@router.post(
    "/register",
    response_model=SuccessMessageResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": APIErrorResponse, "description": "Bad Request"},
        403: {"model": APIErrorResponse, "description": "Forbidden (CSRF error)"},
        500: {"model": APIErrorResponse, "description": "Internal Server Error"},
    }
)
async def register(
    form_data: UserCreate,
    request: Request,
    response: Response,
    db: AsyncIOMotorDatabase = Depends(get_db),
    csrf_protect: CsrfProtect = Depends(),
):
    flow_logger.info("in register endpoint")

    
    try:
        await csrf_protect.validate_csrf(request)
        flow_logger.info("CSRF token validated successfully.")
    except CsrfProtectError:
        flow_logger.error("CSRF token validation failed.")
        raise

    # Check if user already exists
    try:
        if await users_col(db).find_one({"username": form_data.username}):
            flow_logger.info(f"Registration failed: User '{form_data.username}' already exists.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=APIErrorResponse(
                    message="User already exists",
                    error=ErrorDetail(
                        code="USER_EXISTS",
                        details=f"Username '{form_data.username}' is already taken."
                    )
                ).model_dump()
            )
    except HTTPException:
        raise
    except Exception as e:
        flow_logger.error("Database error during user existence check: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=APIErrorResponse(
                message="Error checking user existence.",
                error=ErrorDetail(
                    code="DB_QUERY_ERROR",
                    details=f"A database error occurred: {str(e)}"
                )
            ).model_dump()
        )

    try:
        user_doc = await UserCreateModel(
            username=form_data.username,
            password=form_data.password
        ).doc()
    except HTTPException:
        raise
    except Exception as e:
        flow_logger.error("Error creating user model: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=APIErrorResponse(
                message="Failed to process user data for registration.",
                error=ErrorDetail(
                    code="MODEL_PROCESSING_ERROR",
                    details=f"Error while preparing user data: {str(e)}"
                )
            ).model_dump()
        )

    try:
        res = await users_col(db).insert_one(user_doc)
        rec = await users_col(db).find_one({"_id": res.inserted_id})
    except Exception as e:
        flow_logger.error("Database error during user save/fetch: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=APIErrorResponse(
                message="Error saving new user to database.",
                error=ErrorDetail(
                    code="DB_INSERT_FETCH_ERROR",
                    details=f"A database error occurred: {str(e)}"
                )
            ).model_dump()
        )

    if not rec:
        flow_logger.error("User record not found immediately after successful insert for username: %s", form_data.username)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=APIErrorResponse(
                message="Failed to retrieve user record after creation.",
                error=ErrorDetail(
                    code="USER_POST_INSERT_NOT_FOUND",
                    details="The newly created user record could not be found."
                )
            ).model_dump()
        )

    # Generate authentication tokens and set cookie
    tok_data = TokenData(username=rec["username"])
    access_token = create_access_token(tok_data)
    refresh_token = create_refresh_token(tok_data)

    security_logger.info("User '%s' registered successfully.", rec["username"])
    
    # Set the refresh token as an HttpOnly cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60, # max_age in seconds
        httponly=True,       # Prevents client-side JavaScript access
        secure=True,         # Only send over HTTPS (essential in production)
        samesite="Lax",      # Helps prevent CSRF. "Lax" is a good default.
        # TODO: add domain and path
        # domain="yourdomain.com", # Uncomment and set if needed for cross-subdomain
        # path="/"             # Default, usually not needed unless restricting paths
    )

    # Set the refresh token as an HttpOnly cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60,
        httponly=True,
        secure=True,
        samesite="Lax",
    )

    csrf_protect.unset_csrf_cookie(response)

    # Return success response
    return SuccessMessageResponse(
        message="User registered successfully. Please proceed to login."
    )


# @router.post("/login", summary="Login with username/password")
# async def login_user():
#     # Your login logic here
#     return {"message": "Logged in"}

# @router.post("/logout", summary="Logout + revoke tokens")
# async def logout_user():
#     # Your logout logic here (e.g., revoke refresh token)
#     return {"message": "Logged out"}

# @router.post("/refresh_token", summary="Rotate access token")
# async def refresh_access_token():
#     # Your refresh token logic here
#     return {"message": "Token refreshed"}