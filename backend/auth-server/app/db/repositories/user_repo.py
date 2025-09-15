# app/db/repositories/user_repo.py

from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
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
