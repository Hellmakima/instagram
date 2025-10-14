# auth-server/app/api/api_v1/endpoints/auth/router.py
# Contains /register, /login, /logout, /refresh_token, also /csrf-token for now

from fastapi import (
    APIRouter, 
    Depends, 
    Request, 
    Response, 
    status,
)
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.config import settings
from app.core.csrf import CsrfProtect, verify_csrf
from app.schemas.auth import (
    LoginForm,
    UserCreate,
)
from app.schemas.responses import (
    APIErrorResponse, 
    SuccessMessageResponse,
)
from app.services.auth.user_create import create_user as create_user_service
from app.services.auth.user_login import login_user as login_user_service
from app.services.auth.user_logout import logout_user as logout_user_service
from app.services.auth.user_refresh_token import refresh_access_token as refresh_access_token_service
from app.repositories.refresh_token import RefreshToken as RefreshTokenRepository
from app.repositories.user import User as UserRepository
from app.api.dependencies.db_deps import get_user_repo, get_refresh_token_repo, get_session

import logging
request_logger = logging.getLogger("app_requests")
# TODO: remove below loggers
flow_logger = logging.getLogger("app_flow")
db_logger = logging.getLogger("app_db")

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)  # IP-based rate limiting

# TODO: fix it's place. (decide which file to put this function)
@router.get(
    "/csrf-token",
    response_model=SuccessMessageResponse
)
async def generate_csrf_token(
    response: Response,
    csrf_protect: CsrfProtect = Depends()
):
    csrf_token, signed_token = csrf_protect.generate_csrf_tokens()
    csrf_protect.set_csrf_cookie(signed_token, response)
    return SuccessMessageResponse(
        message="CSRF token generated successfully.",
        data={"csrf_token": csrf_token}
    )


# TODO: implement session=Depends(get_session)

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
@limiter.limit("10/minute")
async def register(
    form_data: UserCreate,
    request: Request, # required by verify_csrf
    _: None = Depends(verify_csrf),
    user_repo: UserRepository = Depends(get_user_repo),
):
    request_logger.info("in register endpoint")
    await create_user_service(form_data, user_repo)
    return SuccessMessageResponse(
        message="User registered successfully. Please proceed to login."
    )


@router.post(
        "/login", 
        summary="Login with username/password",
        response_model=SuccessMessageResponse,
        status_code=status.HTTP_200_OK,
        responses={
            400: {"model": APIErrorResponse, "description": "Bad Request"},
            401: {"model": APIErrorResponse, "description": "Unauthorized"},
            500: {"model": APIErrorResponse, "description": "Internal Server Error"},
        }
)
@limiter.limit("10/hour")
# TODO: use redis and make this rate limiting only for failed attempts and suspend for a while.
async def login(
    form_data: LoginForm,
    request: Request,
    response: Response,
    _: None = Depends(verify_csrf),
    user_repo: UserRepository = Depends(get_user_repo),
    refresh_token_repo: RefreshTokenRepository = Depends(get_refresh_token_repo)
):
    flow_logger.info("in login endpoint")

    client_ip = request.headers.get("x-forwarded-for") or (request.client.host if request.client else "unknown")

    access_token, refresh_token = await login_user_service(
        form_data,
        user_repo,
        refresh_token_repo,
        client_ip
    )

    # Set the refresh token as an HttpOnly cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60, # max_age in seconds
        httponly=True,       # Prevents client-side JavaScript access
        secure=True,         # Only send over HTTPS (essential in production)
        samesite="lax",      # Helps prevent CSRF. "lax" is a good default.
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
        samesite="lax",
    )

    # Return success response
    return SuccessMessageResponse(
        message="Login successful."
    )


@router.post(
        "/logout",
        summary="Logout user",
        response_model=SuccessMessageResponse,
        status_code=status.HTTP_200_OK,
        responses={
            400: {"model": APIErrorResponse, "description": "Bad Request"},
            401: {"model": APIErrorResponse, "description": "Unauthorized"},
            500: {"model": APIErrorResponse, "description": "Internal Server Error"},
        }
)
async def logout(
    request: Request,
    response: Response,
    _: None = Depends(verify_csrf),
    refresh_token_repo: RefreshTokenRepository = Depends(get_refresh_token_repo),
):
    request_logger.info("in logout endpoint")

    access_token = request.cookies.get("access_token", "")
    refresh_token = request.cookies.get("refresh_token", "")

    await logout_user_service(access_token, refresh_token, refresh_token_repo)

    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    return SuccessMessageResponse(message="Logout successful.")



@router.post(
        "/refresh_token", 
        summary="Rotate access token",
        response_model=SuccessMessageResponse,
        status_code=status.HTTP_200_OK,
        responses={
            400: {"model": APIErrorResponse, "description": "Bad Request"},
            401: {"model": APIErrorResponse, "description": "Unauthorized"},
            500: {"model": APIErrorResponse, "description": "Internal Server Error"},
        }
)
async def refresh_access_token(
    request: Request,
    _: None = Depends(verify_csrf),
    refresh_token_repo: RefreshTokenRepository = Depends(get_refresh_token_repo),
    session=Depends(get_session)
):
    flow_logger.info("in refresh token endpoint")

    refresh_token = request.cookies.get("refresh_token", "")

    new_access_token, new_refresh_token = await refresh_access_token_service(
        refresh_token=refresh_token,
        refresh_token_repo=refresh_token_repo,
        session=session
    )

    response = Response(content="OK", media_type="text/plain")
    response.set_cookie(
        key="access_token",
        value=new_access_token,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        httponly=True,
        secure=True,
        samesite="lax",
    )
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        max_age=settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60,
        httponly=True,
        secure=True,
        samesite="lax",
    )

    return SuccessMessageResponse(message="Token refreshed successfully.")
