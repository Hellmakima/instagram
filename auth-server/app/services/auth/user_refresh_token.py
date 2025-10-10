# app/services/auth/user_refresh_token.py

from typing import Tuple
from app.schemas.responses import (
    APIErrorResponse, 
    ErrorDetail, 
    InternalServerError,
)
from app.db.repositories.refresh_token import RefreshToken as RefreshTokenRepository
from app.core.security import verify_token
from fastapi import (
    HTTPException,
    status,
)
from typing import Tuple

from app.schemas.auth import TokenData
from app.core.security import (
    create_access_token,
    create_refresh_token,
)

import logging
flow_logger = logging.getLogger("app_flow")
security_logger = logging.getLogger("security_logger")

async def refresh_access_token(
    refresh_token: str,
    refresh_token_repo: RefreshTokenRepository,
    session
) -> Tuple[str, str]:
    """
    Validate the existing tokens, revoke the old refresh token,
    generate and store a new refresh token, and generate a new access token.
    Returns (new_access_token, new_refresh_token)
    """
    
    flow_logger.info("in refresh token endpoint")
    
    try:
        if not refresh_token:
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
        user = verify_token(token=refresh_token, token_type="refresh")
        flow_logger.info("refresh token verified: %s", str(user.id))
    except HTTPException:
        flow_logger.error("Refresh token not found or expired.")
        raise
    except Exception as e:
        flow_logger.error("Refresh token verification failed: %s", str(e))
        raise InternalServerError()


    async with session.start_transaction():
        try:
            refresh_token_doc = await refresh_token_repo.find_by_token(refresh_token)

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
            flow_logger.info("Found refresh token.")

            await refresh_token_repo.revoke(refresh_token_doc["_id"], session)
            flow_logger.info("Old refresh token revoked successfully.")

            # Generate and insert the new refresh token
            user_token_payload = TokenData(id=user.id)
            new_refresh_token = create_refresh_token(user_token_payload)

            await refresh_token_repo.insert(user.id, new_refresh_token, session)
            flow_logger.info("New refresh token inserted successfully.")

            # Generate new access token
            new_access_token = create_access_token(user_token_payload)

        except HTTPException:
            raise
        except Exception as e:
            flow_logger.error("Transaction failed during token refresh: %s", str(e))
            raise InternalServerError()
    
    return new_access_token, new_refresh_token