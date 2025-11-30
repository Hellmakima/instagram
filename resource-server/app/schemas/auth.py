"""
### File: app/schemas/auth.py

Contains the auth incomming request schema. Describes JSON Structures for frontend requests.
"""

from pydantic import BaseModel, Field


class TokenData(BaseModel):
    id: str = Field(..., description="Unique ID of the user")
