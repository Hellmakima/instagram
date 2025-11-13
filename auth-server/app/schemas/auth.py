"""
### File: app/schemas/auth.py

Contains the auth incomming request schema. Describes JSON Structures for frontend requests.
"""

from datetime import datetime
from pydantic import BaseModel, Field
from app.schemas.user import Id as UserId


class LoginForm(BaseModel):
    username_or_email: str = Field(..., description="Username or email of the user")
    password: str = Field(..., description="Password of the user")
    user_agent: str = Field(..., description="User agent string of the client")


class TokenSub(UserId):
    pass


class TokenData(BaseModel):
    exp: datetime = Field(..., description="Token expiration date")
    sub: TokenSub = Field(..., description="Token data")
    type: str = Field(..., description="Token type")


class BooleanValue(BaseModel):
    # Used for generic boolean requests
    value: bool = Field(..., description="Generic boolean value")
