"""
### File: app/schemas/auth.py

Contains the auth response schema. Describes JSON Structures for frontend requests.
"""

from pydantic import BaseModel, Field
from typing import Optional

class UserCreate(BaseModel):
    username: str = Field(..., description="Username of the user")
    email: str = Field(..., description="Email of the user")
    password: str = Field(..., description="Password of the user")

class LoginForm(BaseModel):
    username_or_email: str = Field(..., description="Username or email of the user")
    password: str = Field(..., description="Password of the user")

class TokenData(BaseModel):
    _id: str = Field(..., description="Username of the user")

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