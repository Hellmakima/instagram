# app/db/repositories/user_repo.py

from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.config import settings

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

    async def insert(self, user_doc: dict) -> Optional[str]:
        flow_logger.info("in insert")
        try:
            res = await self.collection.insert_one(user_doc)
            if res:
                db_logger.info("User record inserted successfully.")
                return res.inserted_id
            db_logger.info("User record not found.")
            return None
        except Exception as e:
            db_logger.error("Database error during user save/fetch: %s", str(e))
            raise

    # async def find_by_id(self, user_id: str) -> Optional[str]:
    #     flow_logger.info("in find_by_id")
    #     try:
    #         rec = await self.collection.find_one({"_id": user_id}, projection={"_id": 1})
    #         if rec:
    #             db_logger.info("User record fetched successfully.")
    #             return rec["_id"]
    #         db_logger.info("User record not found.")
    #         return None
    #     except Exception as e:
    #         db_logger.error("Database error during user save/fetch: %s", str(e))
    #         raise
