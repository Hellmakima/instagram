# app/repositories/user.py

"""
User repository for interacting with the users collection in MongoDB.

Schema
users collection:
{
  "_id": {
    "$oid": "68e8b11430dd07dd064ff1b4"
  },
  "username": "sufiyanhattar",
  "email": "sufiyanhattar@gmail.com",
  "hashed_password": "$2b$12$/8fpXpKoGA.3k/mfq26Y4O0WdRTof0ZwX3GWV0PmkF9kvPAULHGDq",
  "created_at": {
    "$date": "2025-10-10T07:09:08.685Z"
  },
  "is_verified": true,
  "last_activity_at": {
    "$date": "2025-10-10T07:09:08.685Z"
  },
  "suspended_till": {
    "$date": "2025-10-10T13:09:08.685Z"
  } | null,
  "delete_at": {
    "$date": "2025-10-10T13:09:08.685Z"
  } | null
}
"""

from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.config import settings
from bson.objectid import ObjectId
from app.models.auth import (
    UserCreate as UserCreateModel,
    UserId as UserIdModel,
    UserDetailed as UserDetailedModel,
    UserWithPassword as UserWithPasswordModel,
)
from app.repositories.interfaces import UserRepositoryInterface

import logging
flow_logger = logging.getLogger("app_flow")
db_logger = logging.getLogger("app_db")

class User(UserRepositoryInterface):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.get_collection(settings.USER_COLLECTION)


    async def create(self, user_doc: UserCreateModel) -> str:
        flow_logger.info("in insert")
        try:
            # ensure aliases (e.g. `_id`) are used if present on the model
            res = await self.collection.insert_one(user_doc.model_dump(by_alias=True))
            db_logger.info("User record inserted successfully.")
            # return string id to keep interface DB-agnostic
            return str(res.inserted_id)
        except Exception as e:
            db_logger.error("Database error during user insert: %s", str(e))
            raise


    async def get_by_username_or_email(self, identifier: str) -> Optional[UserWithPasswordModel]:
        """
        Get user by username or email.
        Used for login.
        """
        flow_logger.info("in get_by_username_or_email")
        try:
            rec = await self.collection.find_one(
                {"$or": [{"username": identifier}, {"email": identifier}]},
                projection={
                    "_id": 1,
                    "username": 1,
                    "hashed_password": 1,
                    "is_verified": 1,
                    "delete_at": 1,
                    "suspended_till": 1,
                },
            )
            if rec:
                db_logger.info("User record fetched successfully.")
                # construct model via Pydantic to leverage validation/aliases
                return UserWithPasswordModel.model_validate({
                    "_id": rec["_id"],
                    "username": rec.get("username"),
                    "hashed_password": rec.get("hashed_password"),
                    "is_verified": rec.get("is_verified"),
                    "delete_at": rec.get("delete_at"),
                    "suspended_till": rec.get("suspended_till"),
                })
            db_logger.info("User record not found.")
            return None
        except Exception as e:
            db_logger.error("Database error during user existence check: %s", str(e))
            raise


    async def get_verified(self, username: str, email: str) -> Optional[dict]:
        flow_logger.info("in get_verified")
        try:
            rec = await self.collection.find_one(
                {
                    "$and": [
                        {"$or": [{"username": username}, {"email": email}]},
                        {"is_verified": True},
                    ]
                },
                projection={"_id": 1},
            )
            if rec:
                db_logger.info("User record fetched successfully.")
                return rec
            db_logger.info("User record not found.")
            return None
        except Exception as e:
            db_logger.error("Database error during user existence check: %s", str(e))
            raise


    async def get_by_id(self, user_id: str) -> Optional[UserDetailedModel]:
        flow_logger.info("in get_by_id")
        try:
            # validate incoming id before attempting ObjectId conversion
            if not ObjectId.is_valid(user_id):
                db_logger.info("Invalid user_id provided to get_by_id.")
                return None

            rec = await self.collection.find_one(
                {"_id": ObjectId(user_id)},
                projection={
                    "_id": 1,
                    "is_verified": 1,
                    "suspended_till": 1,
                    "delete_at": 1,
                },
            )
            if rec:
                db_logger.info("User record fetched successfully.")
                return UserDetailedModel.model_validate({
                    "_id": rec["_id"],
                    "is_verified": rec.get("is_verified"),
                    "suspended_till": rec.get("suspended_till"),
                    "delete_at": rec.get("delete_at"),
                })
            db_logger.info("User record not found.")
            return None
        except Exception as e:
            db_logger.error("Database error during user existence check: %s", str(e))
            raise


    async def get_by_username(self, username: str) -> Optional[UserIdModel]:
        flow_logger.info("in get_by_username")
        try:
            rec = await self.collection.find_one(
                {"username": username},
                projection={
                    "_id": 1,
                },
            )
            if rec:
                db_logger.info("User record fetched successfully.")
                return UserIdModel.model_validate({"_id": rec["_id"]})
            db_logger.info("User record not found.")
            return None
        except Exception as e:
            db_logger.error("Database error during user existence check: %s", str(e))
            raise


    async def mark_as_verified(self, user_id: str) -> bool:
        """Set is_verified to True for the given user id."""
        flow_logger.info("in mark_as_verified for user %s", user_id)
        try:
            if not ObjectId.is_valid(user_id):
                db_logger.info("Invalid user_id provided to mark_as_verified.")
                return False
            # Mark verified and clear delete_at to prevent automatic deletion
            res = await self.collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"is_verified": True, "delete_at": None}},
            )
            updated = res.modified_count > 0
            if updated:
                db_logger.info("User %s marked as verified.", user_id)
            else:
                db_logger.info("No document updated for user %s.", user_id)
            return updated
        except Exception as e:
            db_logger.error("Database error during mark_as_verified: %s", str(e))
            raise
