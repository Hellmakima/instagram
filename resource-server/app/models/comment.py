# app/models/comment.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CommentModel(BaseModel):
    post_id: str
    user_id: str
    comment: str
    parent_comment_id: Optional[str] = None
    timestamp: datetime

