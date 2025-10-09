# app/db/repositories/refresh_token_repo.py

from datetime import datetime, timezone, timedelta
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.config import settings


class RefreshToken:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.get_collection(settings.REFRESH_TOKEN_COLLECTION)

    async def find_by_token(self, token: str) -> Optional[dict]:
        return await self.collection.find_one(
            {"refresh_token": token},
            projection={"_id": 1, "user_id": 1, "expires_at": 1, "revoked": 1},
        )

    async def insert(self, user_id: str, refresh_token: str, session=None):
        doc = {
            "user_id": user_id,
            "refresh_token": refresh_token,
            "expires_at": datetime.now(timezone.utc)
            + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES),
            "revoked": False,
        }
        return await self.collection.insert_one(doc, session=session)

    async def delete_by_token(self, token: str):
        return await self.collection.delete_one({"refresh_token": token})

    async def revoke(self, token_id, session=None):
        return await self.collection.update_one(
            {"_id": token_id}, {"$set": {"revoked": True}}, session=session
        )
