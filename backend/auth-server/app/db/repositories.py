# app/db/repositories.py

from datetime import datetime, timezone, timedelta
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.config import settings


class RefreshTokenRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.get_collection("refresh_tokens")

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


from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase


class UserRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.get_collection("users")

    async def find_by_username_or_email(self, identifier: str) -> Optional[dict]:
        return await self.collection.find_one(
            {"$or": [{"username": identifier}, {"email": identifier}]},
            projection={
                "_id": 1,
                "hashed_password": 1,
                "is_deleted": 1,
                "is_blocked": 1,
                "is_verified": 1,
            },
        )

    async def find_verified(self, username: str, email: str) -> Optional[dict]:
        return await self.collection.find_one(
            {
                "$and": [
                    {"$or": [{"username": username}, {"email": email}]},
                    {"is_verified": True},
                ]
            },
            projection={"_id": 1},
        )

    async def insert(self, user_doc: dict):
        res = await self.collection.insert_one(user_doc)
        return res

    async def find_by_id(self, user_id: str):
        return await self.collection.find_one({"_id": user_id}, projection={"_id": 1})
