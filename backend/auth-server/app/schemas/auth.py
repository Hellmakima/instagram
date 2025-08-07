"""
### File: app/schemas/auth.py

Contains the auth response schema. Describes JSON Structures for frontend requests.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime, timezone
from app.core.security import get_password_hash
import re

class UserCreate(BaseModel):
    # TODO: id: str = Field(default=uuid.uuid4().hex, description="Unique ID of the user")
    # TODO: decide if username is all lowercase, and if it can include . _ -
    username: str = Field(
        ..., 
        min_length=4, 
        max_length=20, 
        description="Username of the user"
    )
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
            "created_at": self.created_at,
            "email": self.email,
            "is_verified": self.is_verified,
            "is_blocked": self.is_blocked,
            "is_deleted": self.is_deleted
        }
    
    @field_validator('username')
    @classmethod
    def validate_username_characters(cls, v: str) -> str:
        # Allow only alphanumeric characters, periods, underscores, and hyphens.
        if not re.match(r"^[a-zA-Z0-9._-]+$", v):
            # Raise ValueError for Pydantic to catch and convert to 422
            raise ValueError("Username must be alphanumeric and can include periods (.), underscores (_), and hyphens (-).")
        return v

    @field_validator('email')
    @classmethod
    def validate_email_domain(cls, v: str) -> str:
        if not v.endswith("@gmail.com"):
            raise ValueError("We currently only support emails from the gmail.com domain.")
        return v

    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        MIN_PASSWORD_LENGTH = 10
        MAX_PASSWORD_LENGTH = 72 # Common max length for password hashing algorithms

        if len(v) < MIN_PASSWORD_LENGTH:
            raise ValueError(f"Password must be at least {MIN_PASSWORD_LENGTH} characters long.")
        if len(v) > MAX_PASSWORD_LENGTH:
            raise ValueError(f"Password must be less than {MAX_PASSWORD_LENGTH} characters long.")
        
        # Ensure complexity: at least one uppercase, one lowercase, one digit, one special character.
        if not re.search(r'[A-Z]', v):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', v):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r'\d', v):
            raise ValueError("Password must contain at least one number.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v): # Example special characters
            raise ValueError("Password must contain at least one special character.")
            
        return v

class LoginForm(BaseModel):
    username_or_email: str = Field(..., description="Username or email of the user")
    password: str = Field(..., description="Password of the user")

class TokenData(BaseModel):
    id: str = Field(..., description="Username of the user")

class SuccessMessageResponse(BaseModel):
    success: bool = True
    message: str = Field("Success", description="Message of the response")

class ErrorDetail(BaseModel):
    code: str = Field("UNKNOWN_ERROR", description="Error code")
    details: str = Field("No details provided", description="Details of the error")

class APIErrorResponse(BaseModel):
    success: bool = False
    message: str = Field("Error", description="Message of the response")
    error: Optional[ErrorDetail] = None


# Response schema
from fastapi import HTTPException, status
class InternalServerError(HTTPException):
    def __init__(self, details: str = "An unexpected server error occurred."):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=APIErrorResponse(
                message="An unexpected server error occurred.",
                error=ErrorDetail(
                    code="INTERNAL_SERVER_ERROR",
                    details=details
                )
            ).model_dump()
        )