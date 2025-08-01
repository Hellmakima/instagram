# auth-server/app/api/api_v1/endpoints/auth/router.py
# Contains /register, /login, /logout, /refresh_token

from datetime import datetime, timedelta, timezone
from fastapi import (
    APIRouter, 
    Depends, 
    HTTPException, 
    Request, 
    Response, 
    status,
)
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    get_current_user,
    verify_password,
    verify_token,
)
from app.schemas.auth import (
    # LogoutRequest,
    # RefreshUser,
    APIErrorResponse,
    ErrorDetail,
    InternalServerError,
    LoginForm,
    SuccessMessageResponse,
    TokenData,
    UserCreate,
)
from app.models.user import UserCreate as UserCreateModel
from app.core.csrf import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError

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
    csrf_token, signed_token = csrf_protect.generate_csrf_tokens()
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
    '''
    # User Enumeration Risk (Partial):

    The current check if await users_col(db).find_one({"$and": [{"$or": [{"username": form_data.username}, {"email": form_data.email}]}, {"is_verified": True}]}) correctly avoids leaking which specific field (username or email) is taken if an account exists and is verified. This is good.

    Proactive Suggestion: However, if an unverified user exists with the same username/email, the current logic would still allow a new registration, potentially leading to duplicate unverified accounts or race conditions if verification is asynchronous. Consider adding a check for any existing user (verified or unverified) and then handling the "unverified user exists" case differently (e.g., re-sending verification email).
    '''
    flow_logger.info("in register endpoint")
    
    try:
        await csrf_protect.validate_csrf(request)
        flow_logger.info("CSRF token validated successfully.")
    except CsrfProtectError:
        flow_logger.error("CSRF token validation failed.")
        raise

    # Check if user already exists
    try:
        if await users_col(db).find_one({
            "$and": [
                {"$or": [
                    {"username": form_data.username},
                    {"email": form_data.email},
                ]},
                {"is_verified": True},
            ]},
            projection={"_id": 1}
        ):
            flow_logger.info("Registration failed: User with provided username or email already exists.")
            # Do NOT specify which field is taken.
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=APIErrorResponse(
                    message="Username or email is already in use",
                    error=ErrorDetail(
                        code="USER_EXISTS",
                        details="An account with this username or email already exists."
                    )
                ).model_dump()
            )
    except HTTPException:
        raise
    except Exception as e:
        flow_logger.error("Database error during user existence check: %s", str(e))
        raise InternalServerError()

    try:
        user_doc = await UserCreateModel(
            username=form_data.username,
            password=form_data.password,
            email=form_data.email
        ).doc()
    except HTTPException:
        raise
    except Exception as e:
        flow_logger.error("Error creating user model: %s", str(e))
        raise InternalServerError()

    # TODO: add email verification
    # currently, users are set as unverified, need to verify them manually
    '''
    Recommendation: Implement an email verification flow:

        Upon registration, set is_verified to False.

        Generate a unique, time-limited verification token.

        Store this token (hashed) with the user record or in a separate collection.

        Send an email to the user's provided address with a link containing the verification token.

        Create a new endpoint (e.g., /verify-email) that accepts this token, verifies it, and updates is_verified to True.

        Only allow login for is_verified: True users.
    '''

    try:
        res = await users_col(db).insert_one(user_doc)
        flow_logger.info("User record inserted successfully.")
        rec = await users_col(db).find_one({"_id": res.inserted_id}, projection={"_id": 1})
        flow_logger.info("User record fetched successfully.")
    except Exception as e:
        flow_logger.error("Database error during user save/fetch: %s", str(e))
        raise InternalServerError()

    if not rec:
        flow_logger.error("User record not found immediately after successful insert for username: %s", form_data.username)
        raise InternalServerError()

    security_logger.info("User '%s' registered successfully.", rec["username"])
    csrf_protect.unset_csrf_cookie(response)

    # Return success response
    return SuccessMessageResponse(
        message="User registered successfully. Please proceed to login."
    )

# '''
@router.post(
        "/login", 
        summary="Login with username/password",
        response_model=SuccessMessageResponse,
        status_code=status.HTTP_200_OK,
        responses={
            400: {"model": APIErrorResponse, "description": "Bad Request"},
            401: {"model": APIErrorResponse, "description": "Unauthorized"},
            403: {"model": APIErrorResponse, "description": "Forbidden (CSRF error)"},
            500: {"model": APIErrorResponse, "description": "Internal Server Error"},
        }
)
async def login_user(
    form_data: LoginForm,
    request: Request,
    response: Response,
    db: AsyncIOMotorDatabase = Depends(get_db),
    csrf_protect: CsrfProtect = Depends(),
):
    flow_logger.info("in login endpoint")
    try:
        await csrf_protect.validate_csrf(request)
        flow_logger.info("CSRF token validated successfully.")
    except CsrfProtectError:
        flow_logger.error("CSRF token validation failed.")
        raise

    try:
        rec = await users_col(db).find_one({
            "$or": [
                {"username": form_data.username_or_email},
                {"email": form_data.username_or_email}
            ]}, 
            projection={"_id": -1, "hashed_password": 1, "username": 1, "is_deleted": 1, "is_blocked": 1, "is_verified": 1}
        )
    except Exception as e:
        flow_logger.error("Error fetching user from DB: %s", str(e))
        raise InternalServerError()
    if rec:
        is_password_valid = await verify_password(form_data.password, rec.get("hashed_password"))

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
            "Failed login attempt for user '%s'. IP: %s", 
            form_data.username_or_email,
            # request.client.host # Assuming you've fixed the TODO
            # TODO: implement this to add IP address of client. gets complicated if using reverse proxy
        )
        security_logger.warning(
            "Failed login attempt for user '%s'. IP: %s", 
            form_data.username_or_email,
            request.client.host # Assuming you've fixed the TODO
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
    tok_data = TokenData(username=rec["username"])
    access_token = create_access_token(tok_data)
    refresh_token = create_refresh_token(tok_data)

    try:
        await refresh_tokens_col(db).insert_one({
            "user_id": rec["_id"],
            "refresh_token": refresh_token,
            "expires_at": datetime.now(timezone.utc) + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES),
            # TODO: add TTL in mongoDB
            '''
            Token Expiration & Storage:

            MongoDB TTL (TODO: add TTL in mongoDB): This is crucial. Without TTL indexes, your refresh_tokens_col will grow indefinitely, impacting performance and potentially allowing very old tokens to remain in the database even if expired (though your query checks expires_at).

            Recommendation: Add a TTL index to the expires_at field in your refresh_tokens_col collection. Example: db.refresh_tokens.create_index("expires_at", expireAfterSeconds=0).
            '''
            "revoked": False
        })
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

    security_logger.info("User '%s' logged in successfully.", rec["username"])

    # Return success response
    return SuccessMessageResponse(
        message="Login successful."
    )
# '''

@router.post(
        "/logout",
        summary="Logout user",
        response_model=SuccessMessageResponse,
        status_code=status.HTTP_200_OK,
        responses={
            400: {"model": APIErrorResponse, "description": "Bad Request"},
            401: {"model": APIErrorResponse, "description": "Unauthorized"},
            403: {"model": APIErrorResponse, "description": "Forbidden (CSRF error)"},
            500: {"model": APIErrorResponse, "description": "Internal Server Error"},
        }
)
async def logout_user(
    request: Request,
    response: Response,
    csrf_protect: CsrfProtect = Depends(),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    flow_logger.info("in logout endpoint")
    try:
        await csrf_protect.validate_csrf(request)
        flow_logger.info("CSRF token validated successfully.")
    except CsrfProtectError:
        flow_logger.error("CSRF token validation failed.")
        raise

    try:
        verify_token(request.cookies.get("access_token"), token_type="access")
        flow_logger.info("auth token verified.")
    except Exception as e:
        flow_logger.error("Error verifying auth token: %s", str(e))
        raise InternalServerError()
    
    try:
        await refresh_tokens_col(db).delete_one({"refresh_token": request.cookies.get("refresh_token")})
    except Exception as e:
        flow_logger.error("Error deleting refresh token: %s", str(e))
        raise InternalServerError()

    # Unset the refresh token cookie
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    csrf_protect.unset_csrf_cookie(response)

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
            403: {"model": APIErrorResponse, "description": "Forbidden (CSRF error)"},
            500: {"model": APIErrorResponse, "description": "Internal Server Error"},
        }
)
async def refresh_access_token(
    request: Request,
    csrf_protect: CsrfProtect = Depends(),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    flow_logger.info("in refresh token endpoint")
    try:
        await csrf_protect.validate_csrf(request)
        flow_logger.info("CSRF token validated successfully.")
    except CsrfProtectError:
        flow_logger.error("CSRF token validation failed.")
        raise

    try:
        username = get_current_user(request.cookies.get("refresh_token"))
        flow_logger.info("refresh token verified.")
    except HTTPException:
        flow_logger.error("Refresh token not found or expired.")
        raise
    except Exception as e:
        flow_logger.error("Error verifying refresh token: %s", str(e))
        raise InternalServerError()
    
    try:
        if not await refresh_tokens_col(db).find_one({
            "refresh_token": request.cookies.get("refresh_token"),
            "revoked": False,
            "expires_at": {"$gt": datetime.now(timezone.utc)},
        }):
            flow_logger.error("Refresh token not found or expired.")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token not found or expired."
            )
    except Exception as e:
        flow_logger.error("Error checking refresh token: %s", str(e))
        raise InternalServerError()


    try:
        await refresh_tokens_col(db).update_one(
            {"refresh_token": request.cookies.get("refresh_token")},
            {"$set": {"revoked": True}}
        )
    except Exception as e:
        flow_logger.error("Error revoking refresh token: %s", str(e))
        raise InternalServerError()
    
    new_access_token = create_access_token(TokenData(username=request.cookies.get("username")))
    new_refresh_token = create_refresh_token(TokenData(username=request.cookies.get("username")))

    # Set the refresh token as an HttpOnly cookie
    response = Response(content=new_access_token, media_type="text/plain")
    response.set_cookie(
        key="access_token",
        value=new_access_token,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        httponly=True, 
        secure=True,
        samesite="Lax", 
    )
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        max_age=settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60,
        httponly=True,
        secure=True,
        samesite="Lax",
    )

    csrf_protect.unset_csrf_cookie(response)
    
    return SuccessMessageResponse(
        message="Token refreshed."
    )