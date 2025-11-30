# app/repositories/user.py
# TODO: make corresponding changes to AuthServer

"""
User Collection:
- user_id <- FK: comes from auth server
- display_name
- description
- profile_picture
* username is not stored here, its from auth server (single source of truth)
"""

from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.config import settings
from typing import Optional
from app.models.user import User

import logging

db_logger = logging.getLogger("app_db")


class UserRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        """Initialize the UserRepository with the provided database."""
        self.collection = db.get_collection(settings.USER_COLLECTION)

    async def create(self, user_doc: User) -> Optional[str]:
        """Create a new user document."""
        try:
            res = await self.collection.insert_one(user_doc)
            return str(res.inserted_id)  # Return the inserted ID as a string
        except Exception as e:
            db_logger.error(f"Error creating user: {e}")
            raise

    async def get_user(self, user_id: str) -> Optional[dict]:
        """Retrieve the profile information of a user by their ID."""
        profile = await self.collection.find_one(
            {"_id": user_id}, projection={"_id": 1, "username": 1, "profile_picture": 1}
        )
        return profile
