# app/services/user_service.py

from datetime import datetime, timedelta, timezone
from app.schemas.auth import UserCreate # Import your Pydantic model
from app.core.security import get_password_hash # Assuming this is your hashing utility
import uuid

async def prepare_user_for_db(user_create_data: UserCreate) -> dict:
    """
    Prepares a user document for database insertion.
    This includes hashing the password and ensuring all necessary fields are present.
    """
    
    hashed_password = await get_password_hash(user_create_data.password)

    # Construct the dictionary for database insertion
    # All fields from UserCreate should be included, plus the hashed password
    user_doc = {
        "_id": uuid.uuid4().hex,
        "username": user_create_data.username,
        "name": "",
        "email": user_create_data.email,
        "hashed_password":  hashed_password,
        "created_at": datetime.now(timezone.utc),
        "is_verified": False,
        "is_suspended": False,
        "suspended_till": None,
        "last_activity_at": datetime.now(timezone.utc),
        "is_deleted": False,
        # by default, set to delete within a few hours, coz not verified.
        # Remove this once verified.
        "delete_at": datetime.now(timezone.utc) + timedelta(hours=6),
    }
    return user_doc
