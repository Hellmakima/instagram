# app/db/repositories/user_repo.py

from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.config import settings

class UserRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.get_collection(settings.USER_COLLECTION)

    async def insert(self, user_doc: dict):
        res = await self.collection.insert_one(user_doc)
        return res

    async def find_by_id(self, user_id: str):
        return await self.collection.find_one({"_id": user_id}, projection={"_id": 1})
