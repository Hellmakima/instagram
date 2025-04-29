"""
File: app/schemas/user.py

Contains the user schema. Describes JSON Structures for frontend requests
"""

from pydantic import BaseModel, Field
from typing import Optional

class UserBase(BaseModel):
    username: str = Field(..., description="Username of the user")

class UserCreate(UserBase):
    password: str = Field(..., description="Password for the user (during creation only)")

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, description="New username")
    password: Optional[str] = Field(None, description="New password")

class User(UserBase):
    id: str = Field(..., description="Unique identifier for the user (MongoDB)")
    hashed_password: str = Field(..., description="Hashed password", serialization_exclude=True)

    class Config:
        json_encoders = {
            # This is fine if you're using ObjectId inside other models
            # but honestly unnecessary here unless you directly have ObjectId fields
        # ObjectId: str  # Convert ObjectId to string in JSON output
        }
        allow_population_by_field_name = True