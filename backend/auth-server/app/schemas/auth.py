"""
### File: app/schemas/auth.py

Contains the auth response schema. Describes JSON Structures for frontend requests.
"""

from fastapi import HTTPException, status
from pydantic import BaseModel, Field, field_validator
from typing import Optional
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
    password: str = Field(
        ..., 
        min_length=10,
        max_length=72,
        description="Raw password (will be hashed)")
    
    @classmethod
    @field_validator('username')
    def validate_username_characters(cls, v: str) -> str:
        # Allow only alphanumeric characters, periods, underscores, and hyphens.
        if not re.match(r"^[a-zA-Z0-9._-]+$", v):
            # Raise ValueError for Pydantic to catch and convert to 422
            raise ValueError("Username must be alphanumeric and can include periods (.), underscores (_), and hyphens (-).")
        return v

    @classmethod
    @field_validator('email')
    def validate_email_domain(cls, v: str) -> str:
        if not v.endswith("@gmail.com"):
            raise ValueError("We currently only support emails from the gmail.com domain.")
        return v

    @classmethod
    @field_validator('password')
    def validate_password_strength(cls, v: str) -> str:
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
    id: str = Field(..., description="Unique ID of the user")

class SuccessMessageResponse(BaseModel):
    success: bool = True
    message: str = Field("Success", description="Message of the response")
    data: Optional[dict] = {}

class ErrorDetail(BaseModel):
    code: str = Field(default="UNKNOWN_ERROR", description="Error code")
    details: str = Field(default="No details provided", description="Details of the error")

class APIErrorResponse(BaseModel):
    success: bool = Field(default=False, description="Indicates failure")
    message: str = Field(default="Error", description="Message of the response")
    error: Optional[ErrorDetail] = None

class InternalServerError(HTTPException):
    def __init__(self, details: str = "An unexpected server error occurred."):
        error_response = APIErrorResponse(
            message="An unexpected server error occurred.",
            error=ErrorDetail(
                code="INTERNAL_SERVER_ERROR",
                details=details
            )
        )
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response.model_dump()
        )