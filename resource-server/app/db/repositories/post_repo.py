# app/db/repositories/post_repo.py

"""
Posts Collection:
- post_id: the post itself
- user_id: the user who created the post
- timestamp: the timestamp of the post
- shares: the number of shares the post has
- caption: the caption of the post
- type: the type of post (photo, video, text)
- text: the text of the post (If type is text)
- media: [
    {
      "media_id": the media id,
      "type": the type of media (photo, video, text)
    }
  ]
"""

from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.config import settings
from typing import List
