"""
### File: app/schemas/user.py

Contains the user schema
"""
from pydantic import BaseModel, Field

class UserMe(BaseModel):
    """
    Used for testing
    Used for responding to /me endpoint
    """
    username: str = Field(..., description="Username of the user")
    # email: str  # Add other fields you want to expose
