# app/db/repositories/refresh_token_repo.py

from datetime import datetime, timezone, timedelta
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.config import settings

import logging
db_logger = logging.getLogger("app_db")

class RefreshToken:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.get_collection(settings.REFRESH_TOKEN_COLLECTION)

    async def find_by_token(self, token: str) -> Optional[dict]:
        try:
            return await self.collection.find_one(
                {"refresh_token": token, "revoked": False},
                projection={"_id": 1, "user_id": 1, "expires_at": 1, "revoked": 1},
            )
        except Exception as e:
            db_logger.error("Failed to find refresh token for token=%s: %s", token, str(e))
            raise

    async def insert(self, user_id: str, refresh_token: str, session=None):
        doc = {
            "user_id": user_id,
            "refresh_token": refresh_token,
            "expires_at": datetime.now(timezone.utc)
            + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES),
            "revoked": False,
        }
        try:
            return await self.collection.insert_one(doc, session=session)
        except Exception as e:
            db_logger.error("Failed to insert refresh token for user_id=%s: %s", user_id, str(e))
            raise

    async def delete_by_token(self, token: str):
        try:
            return await self.collection.delete_one({"refresh_token": token})
        except Exception as e:
            db_logger.error("Failed to delete refresh token for token=%s: %s", token, str(e))
            raise

    async def revoke(self, token_id, session=None):
        try:
            return await self.collection.update_one(
                {"_id": token_id}, {"$set": {"revoked": True}}, session=session
            )
        except Exception as e:
            db_logger.error("Failed to revoke refresh token for token_id=%s: %s", token_id, str(e))
            raise
