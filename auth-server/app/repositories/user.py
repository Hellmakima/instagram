# app/repositories/user.py

from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.config import settings
from bson.objectid import ObjectId
from app.models.auth import (
    User as UserModel,
    UserOut as UserOutModel,
)

import logging
flow_logger = logging.getLogger("app_flow")
db_logger = logging.getLogger("app_db")

class User:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.get_collection(settings.USER_COLLECTION)

    async def get_by_username_or_email(self, identifier: str) -> Optional[UserOutModel]:
        flow_logger.info("in get_by_username_or_email")
        try:
            rec = await self.collection.find_one(
                {"$or": [{"username": identifier}, {"email": identifier}]},
                projection={
                    "_id": 1,
                    "hashed_password": 1,
                    "is_pending_deletion": 1,
                    "is_suspended": 1,
                    "is_verified": 1,
                },
            )
            if rec:
                db_logger.info("User record fetched successfully.")
                return UserOutModel(
                    id=str(rec["_id"]),
                    hashed_password=rec["hashed_password"],
                    is_pending_deletion=rec["is_pending_deletion"],
                    is_suspended=rec["is_suspended"],
                    is_verified=rec["is_verified"],
                )
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

    async def create(self, user_doc: UserModel) -> ObjectId:
        flow_logger.info("in insert")
        try:
            res = await self.collection.insert_one(user_doc.model_dump())
            db_logger.info("User record inserted successfully.")
            return res.inserted_id
        except Exception as e:
            db_logger.error("Database error during user insert: %s", str(e))
            raise
