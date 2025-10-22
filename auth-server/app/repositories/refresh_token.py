# app/repositories/refresh_token.py

"""
Refresh token collection schema:

{
  "_id": {
    "$oid": "68e8b11430dd07dd064ff1b4"
  },
  "user_id": {
    "$oid": "68e8b11430dd07dd064ff1b4"
  },
  "refresh_token": "some-long-random-string",
  "expires_at": {
    "$date": "2025-10-10T13:09:08.685Z"
  },
  "revoked": false,
  "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
}
"""

from datetime import datetime, timezone, timedelta
from typing import Optional, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.config import settings
from bson import ObjectId
from app.models.refresh_token import RefreshTokenCreate as RefreshTokenCreateModel

import logging
db_logger = logging.getLogger("app_db")

from app.repositories.interfaces import RefreshTokenRepositoryInterface


class RefreshToken(RefreshTokenRepositoryInterface):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.get_collection(settings.REFRESH_TOKEN_COLLECTION)

    async def find_by_token(self, token: str) -> Optional[dict]:
        try:
            return await self.collection.find_one(
                {"refresh_token": token, "revoked": False, "expires_at": {"$gt": datetime.now(timezone.utc)}}, # shouldn't need expires_at check but good to have.
                projection={"_id": 1, "user_id": 1, "expires_at": 1, "revoked": 1},
            )
        except Exception as e:
            db_logger.error("Failed to find refresh token for token=%s: %s", token, str(e))
            raise

    async def insert(self, user_id: str, refresh_token: str, user_agent:str, session: Any = None):
        # if user_id is a valid ObjectId string, store as ObjectId for consistency
        try:
            uid: Any = ObjectId(user_id) if ObjectId.is_valid(user_id) else user_id
        except Exception:
            uid = user_id

        doc = RefreshTokenCreateModel(
            user_id=uid,
            refresh_token=refresh_token,
            expires_at=datetime.now(timezone.utc)
            + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES),
            revoked=False,
            user_agent=user_agent,
        )
        try:
            return await self.collection.insert_one(doc.model_dump(), session=session)
        except Exception as e:
            db_logger.error("Failed to insert refresh token for user_id=%s: %s", user_id, str(e))
            raise

    # TODO: decide what to do with this
    async def delete_by_token(self, token: str):
        try:
            return await self.collection.delete_one({"refresh_token": token})
        except Exception as e:
            db_logger.error("Failed to delete refresh token for token=%s: %s", token, str(e))
            raise

    async def revoke(self, token_id: Any, session: Any = None):
        # ensure token_id is ObjectId when possible
        try:
            tid = ObjectId(token_id) if isinstance(token_id, str) and ObjectId.is_valid(token_id) else token_id
        except Exception:
            tid = token_id

        try:
            return await self.collection.update_one(
                {"_id": tid}, {"$set": {"revoked": True}}, session=session
            )
        except Exception as e:
            db_logger.error("Failed to revoke refresh token for token_id=%s: %s", token_id, str(e))
            raise
