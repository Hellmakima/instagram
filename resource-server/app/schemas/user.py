"""
### File: app/schemas/user.py

Contains the user schema
"""

from pydantic import BaseModel


class User(BaseModel):
    """
    User Id
    """

    id: str


class UserMe(User):
    """
    Used for testing
    Add other fields you want to expose
    """

    username: str
    # email: str  # Add other fields you want to expose


# TODO: place this in a separate file
class Follows(BaseModel):
    """
    Follows Id
    """

    follower_id: str
    following_id: str
