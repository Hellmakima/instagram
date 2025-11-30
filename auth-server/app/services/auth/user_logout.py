# app/services/auth/user_logout.py

from app.schemas.responses import (
    APIErrorResponse,
    ErrorDetail,
    InternalServerError,
)
from app.repositories.interfaces import (
    RefreshTokenRepositoryInterface as RefreshTokenRepository,
)
from app.core.security import verify_token
from fastapi import (
    HTTPException,
    status,
)
from app.schemas.auth import TokenData

# TODO: record user last login in db
import logging

flow_logger = logging.getLogger("app_flow")
security_logger = logging.getLogger("security_logger")


async def logout_user(
    access_token: str,
    refresh_token: str,
    refresh_token_repo: RefreshTokenRepository,
):
    flow_logger.info("in logout endpoint")

    try:
        if access_token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=APIErrorResponse(
                    message="Invalid credentials",
                    error=ErrorDetail(
                        code="INVALID_CREDENTIALS", details="Invalid access token."
                    ),
                ).model_dump(),
            )
        user: TokenData | None = verify_token(token=access_token, token_type="access")
        if not user:
            flow_logger.error(
                "Access token verification failed or returned empty payload"
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=APIErrorResponse(
                    message="Invalid credentials",
                    error=ErrorDetail(
                        code="INVALID_CREDENTIALS", details="Invalid access token."
                    ),
                ).model_dump(),
            )
        flow_logger.info("auth token verified.")
    except Exception as e:
        flow_logger.error("Error verifying auth token: %s", str(e))
        raise InternalServerError()

    try:
        # logout by token string -> delete token record by token
        await refresh_token_repo.delete_by_token(refresh_token)
    except Exception as e:
        flow_logger.error("Error deleting refresh token: %s", str(e))
        raise InternalServerError()

    security_logger.info("User '%s' logged out successfully.", str(user.id))
