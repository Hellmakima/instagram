# app/schemas/comment.py

from pydantic import BaseModel, Field
from typing import Optional

# Used for input validation when a user submits a new comment
class CommentCreate(BaseModel):
    # Enforces a content limit (e.g., max 2000 characters)
    comment: str = Field(min_length=1, max_length=2000)

    # The ID of the post the comment belongs to.
    # We expect a string representation of a MongoDB ObjectId (or a UUID).
    post_id: str

    # Optional: If this comment is a reply, this holds the parent comment's ID.
    parent_comment_id: Optional[str] = None

    # NOTE: user_id and timestamp are intentionally omitted here. 
    # They should be inserted by the server for security (Principle 1).
    # TODO: add user_id and timestamp via some service