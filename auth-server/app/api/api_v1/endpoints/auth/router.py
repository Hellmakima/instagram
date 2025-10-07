# auth-server/app/api/api_v1/endpoints/auth/router.py
# Contains /register, /login, /logout, /refresh_token, also /csrf-token for now

from fastapi import (
    APIRouter, 
    Depends, 
    HTTPException, 
    Request, 
    Response, 
    status,
)
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
    verify_token,
)
from app.core.csrf import CsrfProtect, verify_csrf
from app.schemas.auth import (
    LoginForm,
    TokenData,
    UserCreate,
)
from app.schemas.responses import (
    APIErrorResponse, 
    ErrorDetail, 
    InternalServerError, 
    SuccessMessageResponse,
)
from app.services.user_create import create_user
from app.db.repositories.refresh_token_repo import RefreshTokenRepository
from app.db.repositories.user_repo import UserRepository
from app.api.dependencies.db_deps import get_user_repo, get_refresh_token_repo, get_session

import logging
request_logger = logging.getLogger("app_requests")
# TODO: remove below loggers
flow_logger = logging.getLogger("app_flow")
security_logger = logging.getLogger("security_logger")
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
    await create_user(form_data, user_repo)
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

    try:
        rec = await user_repo.find_by_username_or_email(form_data.username_or_email)
        flow_logger.info("Fetched user record: %s", str(rec))
    except Exception as e:
        flow_logger.error("Error fetching user from DB: %s", str(e))
        raise InternalServerError()
    is_password_valid = False
    if rec:
        is_password_valid = await verify_password(form_data.password, rec.get("hashed_password", ""))
        flow_logger.info("Password verification result: %s", str(is_password_valid))

    # Generic check for ALL failure conditions to prevent user enumeration
    # TODO: maybe separate this based on condition, Gemini says it's a risk to leak this.
    if (
        not rec 
        or not is_password_valid 
        or rec.get("is_deleted") 
        or rec.get("is_blocked") 
        or not rec.get("is_verified")
    ):
        '''
        # IP Address Logging (TODO: implement this to add IP address of client):

        Correction: request.client.host will give you the direct client IP. If you're behind a reverse proxy (like Nginx, AWS ALB, Cloudflare), you must use request.headers.get("x-forwarded-for") or similar headers, as request.client.host will show the proxy's IP.

        Recommendation: Implement robust IP address logging. If using a reverse proxy, ensure it's configured to pass the X-Forwarded-For header correctly, and your application trusts this header. Add an X-Real-IP header if X-Forwarded-For is not sufficient.
        '''
        # request.headers.get("x-forwarded-for", request.client.host)
        flow_logger.info(
            "Failed login attempt for user '%s'. IP: %s. Details: %s",
            form_data.username_or_email,
            request.client.host if request.client else "unknown",
            {"password_valid": is_password_valid, "rec": rec}
            # TODO: implement this to add IP address of client. gets complicated if using reverse proxy
        )
        security_logger.warning(
            "Failed login attempt for user '%s'. IP: %s", 
            form_data.username_or_email,
            request.client.host if request.client else "unknown"
            # TODO: implement this to add IP address of client. gets complicated if using reverse proxy
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=APIErrorResponse(
                message="Invalid credentials",
                error=ErrorDetail(
                    code="INVALID_CREDENTIALS",
                    details="Invalid username, password, or account status."
                )
            ).model_dump()
        )

    # Generate authentication tokens and set cookie
    tok_data = TokenData(id=rec["_id"])
    access_token = create_access_token(tok_data)
    refresh_token = create_refresh_token(tok_data)

    try:
        # TODO: add TTL in mongoDB
        '''
        Token Expiration & Storage:
        MongoDB TTL (TODO: add TTL in mongoDB): This is crucial. Without TTL indexes, your refresh_tokens_col will grow indefinitely, impacting performance and potentially allowing very old tokens to remain in the database even if expired (though your query checks expires_at).
        Recommendation: Add a TTL index to the expires_at field in your refresh_tokens_col collection. Example: db.refresh_tokens.create_index("expires_at", expireAfterSeconds=0).
        '''
        await refresh_token_repo.insert(rec["_id"], refresh_token)
    except Exception as e:
        flow_logger.error("Error saving refresh token to DB: %s", str(e))
        raise InternalServerError()

    
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

    security_logger.info("User '%s' logged in successfully.", rec["_id"])

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
    flow_logger.info("in logout endpoint")

    try:
        token = request.cookies.get("access_token")
        if token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=APIErrorResponse(
                    message="Invalid credentials",
                    error=ErrorDetail(
                        code="INVALID_CREDENTIALS",
                        details="Invalid access token."
                    )
                ).model_dump()
            )
        user = verify_token(token=token, token_type="access")
        flow_logger.info("auth token verified.")
    except Exception as e:
        flow_logger.error("Error verifying auth token: %s", str(e))
        raise InternalServerError()
    
    try:
        await refresh_token_repo.delete_by_token(request.cookies.get("refresh_token", ""))
        db_logger.info("Refresh token deleted successfully.")
    except Exception as e:
        db_logger.error("Error deleting refresh token: %s", str(e))
        flow_logger.error("Error deleting refresh token: %s", str(e))
        raise InternalServerError()

    # Unset the refresh token cookie
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    security_logger.info("User '%s' logged out successfully.", user.id)

    return SuccessMessageResponse(
        message="Logout successful."
    )


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

    try:
        token = request.cookies.get("access_token")
        if token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=APIErrorResponse(
                    message="Invalid credentials",
                    error=ErrorDetail(
                        code="INVALID_CREDENTIALS",
                        details="Invalid access token."
                    )
                ).model_dump()
            )
        user = verify_token(token=token, token_type="access")
        flow_logger.info("refresh token verified.")
    except HTTPException:
        flow_logger.error("Refresh token not found or expired.")
        raise
    except Exception as e:
        flow_logger.error("Error verifying refresh token: %s", str(e))
        raise InternalServerError()

    async with session.start_transaction():
        try:
            refresh_token_doc = await refresh_token_repo.find_by_token(request.cookies.get("refresh_token", ""))

            if not refresh_token_doc:
                flow_logger.warning("Revoked or invalid refresh token used for refresh attempt.")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=APIErrorResponse(
                        message="Unauthorized",
                        error=ErrorDetail(
                            code="REFRESH_TOKEN_INVALID",
                            details="Refresh token not found, revoked, or expired."
                        )
                    ).model_dump()
                )
            db_logger.info("Found refresh token.")

            await refresh_token_repo.revoke(refresh_token_doc["_id"])
            db_logger.info("Old refresh token revoked successfully.")

            # Generate and insert the new refresh token
            user_token_payload = TokenData(id=user.id)
            new_refresh_token = create_refresh_token(user_token_payload)

            await refresh_token_repo.insert(user.id, new_refresh_token)
            db_logger.info("New refresh token inserted successfully.")

            # Generate new access token
            new_access_token = create_access_token(user_token_payload)

        except HTTPException:
            raise
        except Exception as e:
            db_logger.error("Transaction failed during token refresh: %s", str(e))
            raise InternalServerError()
    
    # Set the new tokens
    response = Response(content=new_access_token, media_type="text/plain")
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

    return SuccessMessageResponse(
        message="Token refreshed successfully."
    )