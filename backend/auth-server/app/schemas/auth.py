"""
### File: app/schemas/auth.py

Contains the auth response schema. Describes JSON Structures for frontend requests.
"""

from pydantic import BaseModel, Field
from typing import Optional

class UserCreate(BaseModel):
    username: str = Field(..., description="Username of the user")
    password: str = Field(..., description="Password of the user")

class TokenData(BaseModel):
    username: str = Field(..., description="Username of the user")

class SuccessMessageResponse(BaseModel):
    success: bool = True
    message: str = Field("Success", description="Message of the response")

class ErrorDetail(BaseModel):
    code: str = Field("UNKNOWN_ERROR", description="Error code")
    details: str = Field("No details provided", description="Details of the error")

class APIErrorResponse(BaseModel):
    success: bool = False
    message: str
    error: Optional[ErrorDetail] = None

class RefreshUser(BaseModel):
    refresh_token: str = Field(..., description="Refresh token")
    token_type: str = Field("Bearer", description="Type of token")

class LogoutRequest(BaseModel):
    refresh_token: str
    token_type: str