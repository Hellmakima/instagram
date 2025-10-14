# app/repositories/comment_like.py

"""
Comment Likes Collection:
- comment_id: the comment being liked
- user_id: the user who likes a post
"""

from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.config import settings
from typing import List


class CommentLikeRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.get_collection(settings.COMMENT_LIKES_COLLECTION)

    async def create(self, comment_id: str, user_id: str):
        """Create a like relationship where `user_id` likes `comment_id`."""
        res = await self.collection.insert_one({
            "comment_id": comment_id, 
            "user_id": user_id
        })
        return res

    async def get_likes(self, comment_id: str) -> List[dict]:
        """Get a list of users who like the given comment."""
        return await self.collection.find({"comment_id": comment_id}).to_list(length=None)

    async def get_likes_count(self, comment_id: str) -> int:
        """Get the count of likes for the given comment."""
        return await self.collection.count_documents({"comment_id": comment_id})
    