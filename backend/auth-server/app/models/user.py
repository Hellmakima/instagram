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
    username: str = Field(..., min_length=3, max_length=20, description="Username of the user")

    @field_validator('username')
    def username_must_be_alphanumeric(cls, v):
        if not 4 < len(v) < 20:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "message": "Username must be between 4 and 20 characters long",
                    "error": {
                        "code": "USERNAME_LENGTH",
                        "details": "Username must be between 4 and 20 characters long"
                    }
                }
            )
        # allow only alphanumeric characters and . _
        if not re.match(r"^[a-zA-Z0-9_.-]+$", v): # re.match(r"^[a-zA-Z]+$", v):
            # raise ValueError("Username must be alphanumeric and can include . _ -")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "message": "Username must be alphanumeric and can include . _ -",
                    "error": {
                        "code": "PASSWORD_TOO_SHORT",
                        "details": "Username must be alphanumeric and can include . _ -"
                    }
                }
            )
        return v

class UserCreate(UserBase): # same can be used for update user.
    #TODO: _id: str = Field(default=uuid.uuid4().hex, description="Unique ID of the user")
    email: str = Field(..., description="Email of the user")
    password: str = Field(..., description="Raw password (will be hashed)")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Timestamp of user creation")
    is_verified: bool = False
    is_blocked: bool = False
    is_deleted: bool = False
    
    async def doc(self):
        return {
            "username": self.username,
            "hashed_password": await get_password_hash(self.password),
            "created_at": self.created_at
        }
    
    @field_validator('email')
    def email_must_be_valid(cls, value):
        if not re.match(r"^[\w\.-]+@gmail\.com$", value):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "message": "Email must be valid",
                    "error": {
                        "code": "INVALID_EMAIL",
                        "details": "We currently only support emails from gmail.com domain"
                    }
                }
            )

    @field_validator('password')
    def password_must_be_strong(cls, value):
        if len(value) < 4:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "message": "Password must be at least 4 characters long",
                    "error": {
                        "code": "PASSWORD_TOO_SHORT",
                        "details": "Password must be at least 4 characters long"
                    }
                }
            )
        if len(value) > 50:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "message": "Password must be less than 50 characters long",
                    "error": {
                        "code": "PASSWORD_TOO_LONG",
                        "details": "Password must be less than 50 characters long"
                    }
                }
            )
        if not re.search(r'[A-Z]', value) or not re.search(r'[a-z]', value) or not re.search(r'\d', value):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "message": "Password must contain at least one uppercase letter, one lowercase letter, and one number",
                    "error": {
                        "code": "PASSWORD_NO_UPPERCASE_LETTER",
                        "details": "Password must contain at least one uppercase letter, one lowercase letter, and one number"
                    }
                }
            )
        return value
    
