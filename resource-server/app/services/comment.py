from typing import List, Optional
from datetime import datetime, timezone

# Assuming your repository and models/schemas are available
from app.repositories.comment_repo import CommentRepository
from app.schemas.comment import CommentCreate
from app.models.comment import CommentModel # Assuming this is the final DB-ready model

# IMPORTANT NOTE: 
# The actual database model should use datetime for timestamp and PyObjectId for ID. 
# We assume the CommentRepository interacts with a robust DB model.
# For demonstration, we will use the CommentCreate input and server-side data.

from bson import ObjectId

class CommentService:
    """
    Handles all business logic related to Comments, coordinating
    between the API layer and the data layer (Repository).
    """
    def __init__(self, comment_repo: CommentRepository):
        """Initializes the service with a CommentRepository instance."""
        self.repo = comment_repo

    async def create_comment(self, comment_data: CommentCreate, user_id: str) -> ObjectId:
        """
        Transforms client input and server-injected data into a database document 
        and persists it.

        Args:
            comment_data: The validated Pydantic model from the client (contains comment text, post_id, parent_comment_id).
            user_id: The ID of the authenticated user, extracted securely from the JWT.
        
        Returns:
            The created comment document from the database.
        """
        # 1. Prepare data for database insertion
        # This is where we inject server-controlled, immutable data.
        # comment_doc = {
        #     "comment": comment_data.comment,
        #     "post_id": comment_data.post_id,
        #     "user_id": user_id,  # CRITICAL: Server injects user_id for security
        #     "timestamp": datetime.now(timezone.utc), # CRITICAL: Server injects immutable timestamp (UTC)
        #     "parent_comment_id": comment_data.parent_comment_id,
        # }
        comment_doc = CommentModel(
            comment=comment_data.comment,
            post_id=comment_data.post_id,
            user_id=user_id,  # CRITICAL: Server injects user_id for security
            timestamp=datetime.now(timezone.utc), # CRITICAL: Server injects immutable timestamp (UTC)
            parent_comment_id=comment_data.parent_comment_id,
        )
        
        # 2. Call the repository to perform the database operation
        # The repository handles the BSON serialization and MongoDB insert
        # new_comment_db = await self.repo.insert_one(comment_doc)
        new_comment_db = await self.repo.create(comment_doc)
        
        # 3. Return the result mapped to the external CommentModel
        # (The repository should handle mapping the MongoDB document back to CommentModel)
        return new_comment_db

    async def get_comments_paginated(
        self, 
        post_id: str, 
        limit: int = 20, 
        skip: int = 0
    ) -> List[CommentModel]:
        """
        Fetches comments for a specific post with mandatory pagination.

        Args:
            post_id: The ID of the post to retrieve comments for.
            limit: The maximum number of comments to return (default 20).
            skip: The number of comments to skip (offset for pagination).
        
        Returns:
            A list of CommentModel documents.
        """
        # Business logic can enforce stricter limits here if needed (e.g., max 50).
        if limit > 50:
            limit = 50
            
        # Call the repository to fetch the data. 
        # The repository should handle the indexing, sorting, and pagination logic.
        comments = await self.repo.get_by_post_id(
            post_id=post_id,
            limit=limit,
            skip=skip
        )
        
        return comments

    # You could add other methods here, like:
    # async def delete_comment(self, comment_id: str, user_id: str):
    #     """Ensures the requesting user owns the comment before deletion."""
    #     # Logic: Check ownership -> Call repo.delete_one()
