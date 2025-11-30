"""
### File: app/models/user.py

Contains the user models for db repositories
"""

from pydantic import BaseModel


class User(BaseModel):
    user_id: str
    description: str
    profile_picture: str
    display_name: str


# TODO: place this in a separate file
class Follows(BaseModel):
    follower_id: str
    following_id: str
