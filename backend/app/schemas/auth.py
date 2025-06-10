"""
### File: app/schemas/auth.py

Contains the auth response schema. Describes JSON Structures for frontend requests.
"""

from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    username: str = Field(..., description="Username of the user")
    password: str = Field(..., description="Password of the user")

class TokenData(BaseModel):
    username: str = Field(..., description="Username of the user")

class AuthResponse(BaseModel):
    username: str = Field(..., description="Username of the user")
    access_token: str = Field(..., description="Access token for the user")
    refresh_token: str = Field(..., description="Refresh token")
    token_type: str = Field("Bearer", description="Type of token")

class RefreshUser(BaseModel):
    refresh_token: str = Field(..., description="Refresh token")
    token_type: str = Field("Bearer", description="Type of token")

class LogoutRequest(BaseModel):
    refresh_token: str
    token_type: str