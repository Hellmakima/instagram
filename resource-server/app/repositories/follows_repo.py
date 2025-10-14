# app/repositories/follows.py

"""
Follows Collection:
- follower_id: the user who follows another user
- following_id: the user being followed
"""

from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.config import settings
from typing import List, Optional
from app.models.user import Follows

class FollowRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.get_collection(settings.FOLLOWS_COLLECTION)

    async def create(self, follows_doc: Follows) -> Optional[str]:
        """Create a follow relationship where `follower_id` follows `following_id`."""
        res = await self.collection.insert_one(follows_doc.model_dump())
        return res

    async def get_followers(self, user_id: str) -> List[dict]:
        """Get a list of users who follow the given user (followers)."""
        return await self.collection.find({"following_id": user_id}).to_list(length=None)

    async def get_followers_count(self, user_id: str) -> int:
        """Get the count of followers for the given user."""
        return await self.collection.count_documents({"following_id": user_id})

    async def get_following(self, user_id: str) -> List[dict]:
        """Get a list of users that the given user is following."""
        return await self.collection.find({"follower_id": user_id}).to_list(length=None)

    async def get_following_count(self, user_id: str) -> int:
        """Get the count of users that the given user is following."""
        return await self.collection.count_documents({"follower_id": user_id})
