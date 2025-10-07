# app/db/repositories/user_repo.py

from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.config import settings
from bson.objectid import ObjectId
from app.models.auth import User

import logging
flow_logger = logging.getLogger("app_flow")
db_logger = logging.getLogger("app_db")

class UserRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.get_collection(settings.USER_COLLECTION)

    async def find_by_username_or_email(self, identifier: str) -> Optional[dict]:
        flow_logger.info("in find_by_username_or_email")
        try:
            rec = await self.collection.find_one(
                {"$or": [{"username": identifier}, {"email": identifier}]},
                projection={
                    "_id": 1,
                    "hashed_password": 1,
                    "is_deleted": 1,
                    "is_blocked": 1,
                    "is_verified": 1,
                },
            )
            if rec:
                db_logger.info("User record fetched successfully.")
                return rec
            db_logger.info("User record not found.")
            return None
        except Exception as e:
            db_logger.error("Database error during user existence check: %s", str(e))
            raise

    async def find_verified(self, username: str, email: str) -> Optional[dict]:
        flow_logger.info("in find_verified")
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

    async def insert(self, user_doc: User) -> ObjectId:
        flow_logger.info("in insert")
        try:
            res = await self.collection.insert_one(user_doc.model_dump())
            db_logger.info("User record inserted successfully.")
            return res.inserted_id
        except Exception as e:
            db_logger.error("Database error during user insert: %s", str(e))
            raise

