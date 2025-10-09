# app/services/user.py

from datetime import datetime, timedelta, timezone
from app.schemas.auth import UserCreate
from app.models.auth import User as UserModel
from app.schemas.responses import (
    APIErrorResponse, 
    ErrorDetail, 
    InternalServerError,
)
from app.db.repositories.user import User as UserRepository
from app.core.security import get_password_hash
from fastapi import (
    HTTPException,
    status,
)
import logging
flow_logger = logging.getLogger("app_flow")
security_logger = logging.getLogger("security_logger")

# TODO: maybe break this into smaller functions
async def create_user(
    form_data: UserCreate,
    user_repo: UserRepository,
):
    """
    Creates a new user in the database.
    """

    # Check if user already exists
    try:
        if await user_repo.find_verified(form_data.username, form_data.email):
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
    
    # TODO: add email verification
    # currently, users are set as unverified, need to verify them manually
    # After this, call resource-server to create new user.
    '''
    Recommendation: Implement an email verification flow:

        Upon registration, set is_verified to False.

        Generate a unique, time-limited verification token.

        Store this token (hashed) with the user record or in a separate collection.

        Send an email to the user's provided address with a link containing the verification token.

        Create a new endpoint (e.g., /verify-email) that accepts this token, verifies it, and updates is_verified to True.
    '''

    hashed_password = await get_password_hash(form_data.password)

    user_doc = UserModel(
        username=form_data.username,
        email=form_data.email,
        hashed_password=hashed_password,
        created_at=datetime.now(timezone.utc),
        is_verified=False,
        is_suspended=False,
        suspended_till=None,
        last_activity_at=datetime.now(timezone.utc),
        is_deleted=True,
        # by default, set to delete within a few minutes, coz not verified.
        # same time as email link expiry.
        # Remove this once verified.
        delete_at=datetime.now(timezone.utc) + timedelta(hours=6),
    )

    try:
        res = await user_repo.insert(user_doc)
        flow_logger.info("User record inserted successfully.")
    except Exception as e:
        flow_logger.error("Database error during user save/fetch: %s", str(e))
        raise InternalServerError()

    security_logger.info("New user registered successfully with id '%s'.", res)
