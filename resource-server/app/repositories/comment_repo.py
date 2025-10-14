# app/repositories/comment.py

"""
Comments Collection:
- comment_id: the comment itself
- post_id: the post the comment is on
- user_id: the user who created the comment
- reply_to: null if the comment is not a reply or the id of the parent comment
- timestamp: the timestamp of the comment
"""

from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.config import settings
from typing import List, Optional
from pymongo.errors import PyMongoError
from app.models.comment import CommentModel
from bson import ObjectId # Import ObjectId for validation (crucial)

class CommentRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.get_collection(settings.COMMENTS_COLLECTION)

    async def create(self, comment_doc: CommentModel) -> Optional[str]:
        """Create a new comment document."""
        try:
            res = await self.collection.insert_one(comment_doc.model_dump())
            return str(res.inserted_id)  # Return the inserted ID as a string
        except PyMongoError as e:
            # Handle database error (e.g., connection issues, duplicate key errors)
            raise Exception(f"Error creating comment: {e}")
    

    async def get_comments(self, post_id: str) -> List[CommentModel]:
        """
        Get a list of comments for the given post.

        @param post_id: The unique identifier for the Post.
        @return: A list of CommentModel documents.
        """
        # Ensure post_id is a valid MongoDB ObjectId or UUID before querying.
        try:
            # If you are using MongoDB's ObjectId for post_id:
            if not ObjectId.is_valid(post_id):
                raise ValueError("Invalid post_id format.")
        except Exception as e:
            # Raise an appropriate exception that FastAPI can catch and return a 400
            raise ValueError(f"Invalid ID provided: {e}")

        # Ensure self.collection is the correct MongoDB collection object
        return await self.collection.find({"post_id": post_id}).to_list(length=None)
    
    async def get_comments_paginated(self, post_id: str, limit: int = 20, skip: int = 0) -> List[CommentModel]:
        # ... ID Validation logic ...

        # Scalable Query:
        cursor = self.collection \
            .find({"post_id": post_id}) \
            .sort([("timestamp", 1)]) \
            .skip(skip) \
            .limit(limit)

        return await cursor.to_list(length=limit)