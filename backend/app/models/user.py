"""
### File: app/models/user.py

Contains the user model. Describe Database Schemas for backend DB server
I'm using it for data validation
"""
from fastapi import HTTPException, status
from pydantic import BaseModel, Field, field_validator
from datetime import datetime, timezone
import re
from app.core.security import get_password_hash


class UserBase(BaseModel):
    # TODO: decide if username is all lowercase, and if it can include . _ -
    username: str = Field(..., min_length=3, max_length=50, description="Username of the user")

    @field_validator('username')
    def username_must_be_alphanumeric(cls, v):
        if not re.match(r"^[a-zA-Z]+$", v): # or not re.match(r"^[a-zA-Z0-9_.-]+$", v):
            raise ValueError("Username must be alphanumeric and can include . _ -")
        return v

class UserCreate(UserBase): # same can be used for update user.
    password: str = Field(..., description="Raw password (will be hashed)")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Timestamp of user creation")

    def doc(self):
        print(self.username)
        return {
            "username": self.username,
            "hashed_password": get_password_hash(self.password),
            "created_at": self.created_at
        }

    @field_validator('password')
    def password_must_be_strong(cls, v):
        if len(v) < 4:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 4 characters long"
            )
        if len(v) > 50:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at most 50 characters long"
            )
        if not re.search(r'[A-Z]', v) or not re.search(r'[a-z]', v) or not re.search(r'\d', v):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must include upper, lower case letters and digits"
            )
        return v
    
