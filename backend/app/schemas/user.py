"""
File: app/schemas/user.py

Contains the user schema
"""
from pydantic import BaseModel

class UserMe(BaseModel):
    """
    Used for testing
    Used for responding to /me endpoint
    """
    username: str
    # email: str  # Add other fields you want to expose
