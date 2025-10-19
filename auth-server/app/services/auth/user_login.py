# app/services/auth/user_login.py

from typing import Tuple
from app.schemas.auth import LoginForm
from app.schemas.responses import (
    APIErrorResponse, 
    ErrorDetail, 
    InternalServerError,
)
from app.repositories.interfaces import UserRepositoryInterface as UserRepository
from app.repositories.interfaces import RefreshTokenRepositoryInterface as RefreshTokenRepository
from app.core.security import verify_password
from fastapi import (
    HTTPException,
    status,
)

from app.schemas.auth import TokenData
from app.core.security import (
    create_access_token,
    create_refresh_token,
)

import logging
flow_logger = logging.getLogger("app_flow")
security_logger = logging.getLogger("security_logger")

async def login_user(
    form_data: LoginForm,
    user_repo: UserRepository,
    refresh_token_repo: RefreshTokenRepository,
    client_ip: str,
) -> Tuple[str, str]:
    flow_logger.info("in login endpoint")

    try:
        rec = await user_repo.get_by_username_or_email(form_data.username_or_email)
        flow_logger.info("Fetched user record: %s", str(rec))
    except Exception as e:
        flow_logger.error("Error fetching user from DB: %s", str(e))
        raise InternalServerError()
    is_password_valid = False
    if rec:
        is_password_valid = await verify_password(form_data.password, rec.hashed_password)
        flow_logger.info("Password verification result: %s", str(is_password_valid))

    # Generic check for ALL failure conditions to prevent user enumeration
    # TODO: maybe separate this based on condition, Gemini says it's a risk to leak this.
    if (
        not rec 
        or not is_password_valid 
        or not rec.is_verified
        or rec.suspended_till
        or rec.delete_at
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
            client_ip,
            {"password_valid": is_password_valid, "rec": rec}
        )
        security_logger.warning(
            "Failed login attempt for user '%s'. IP: %s",
            form_data.username_or_email,
            client_ip
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
    # ensure tokens use string ids (DB-agnostic)
    tok_data = TokenData(id=str(rec.id))
    access_token = create_access_token(tok_data)
    refresh_token = create_refresh_token(tok_data)
    if not access_token or not refresh_token:
        flow_logger.error("Error creating access or refresh token.")
        raise InternalServerError()

    try:
        '''
        Token Expiration & Storage:
        MongoDB TTL (TODO: add TTL in mongoDB): This is crucial. Without TTL indexes, your refresh_tokens_col will grow indefinitely, impacting performance and potentially allowing very old tokens to remain in the database even if expired (though your query checks expires_at).
        Recommendation: Add a TTL index to the expires_at field in your refresh_tokens_col collection. Example: db.refresh_tokens.create_index("expires_at", expireAfterSeconds=0).
        '''
        await refresh_token_repo.insert(str(rec.id), refresh_token)
    except Exception as e:
        flow_logger.error("Error saving refresh token to DB: %s", str(e))
        raise InternalServerError()

    security_logger.info("User '%s' logged in successfully.", str(rec.id))

    return access_token, refresh_token
