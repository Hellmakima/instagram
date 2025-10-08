# app/db/repositories/post_like_repo.py

"""
Post Likes Collection:
- user_id: the user who likes a post
- post_id: the post being liked
"""

from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.config import settings
from typing import List


class PostLikeRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.get_collection(settings.POST_LIKES_COLLECTION)

    async def create(self, user_id: str, post_id: str):
        """Create a like relationship where `user_id` likes `post_id`."""
        res = await self.collection.insert_one({
            "user_id": user_id, 
            "post_id": post_id
        })
        return res

    async def get_likes(self, post_id: str) -> List[dict]:
        """Get a list of users who like the given post."""
        return await self.collection.find({"post_id": post_id}).to_list(length=None)

    async def get_likes_count(self, post_id: str) -> int:
        """Get the count of likes for the given post."""
        return await self.collection.count_documents({"post_id": post_id})