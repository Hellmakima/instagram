"""
File: app/models/user.py

Contains the user model. Describe Database Schemas for backend DB server
"""
from pydantic import BaseModel, Field
from typing import Optional
# from datetime import datetime

class UserBase(BaseModel):
    username: str = Field(..., description="Username of the user")
    # No password here, we don't store plain text!


class UserCreate(UserBase): # same can be used for update user.
    password: str = Field(..., description="Password for the user (during creation only)")


class User(UserBase):
    id: str = Field(..., description="Unique identifier for the user (from MongoDB)")
    hashed_password: str = Field(..., description="Hashed password (stored in DB)")
    # is_active: bool = Field(default=True, description="Whether the user is active")
    # created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of user creation")

    class Config:
        from bson import ObjectId
        json_encoders = {
            ObjectId: str  # Convert ObjectId to string in JSON output
        }
#pilot
"""
File: app/models/user.py

Contains the user model. Describe Database Schemas for backend DB server
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime  # Uncommented as it might be useful for timestamp fields

class UserBase(BaseModel):
    username: str = Field(..., description="Username of the user")
    # No password here, we don't store plain text!

class UserCreate(UserBase):  # Same class can be used for updating user details.
    password: str = Field(..., description="Password for the user (during creation only)")

class User(UserBase):
    id: str = Field(..., description="Unique identifier for the user (from MongoDB)")
    hashed_password: str = Field(..., description="Hashed password (stored in DB)")
    is_active: bool = Field(default=True, description="Whether the user is active")  # Uncommented this line
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of user creation")  # Uncommented this line

    class Config:
        from bson import ObjectId
        json_encoders = {
            ObjectId: str  # Convert ObjectId to string in JSON output
        }
