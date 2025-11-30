# app/models/refresh_token.py

from datetime import datetime

# from typing import Optional
from pydantic import BaseModel, field_validator
from bson import ObjectId


class RefreshTokenCreate(BaseModel):
    """
    Used for creating a new refresh token.
    """

    user_id: str
    refresh_token: str
    expires_at: datetime
    revoked: bool
    user_agent: str

    @field_validator("user_id", mode="before")
    def _normalize_user_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v


class RefreshTokenOut(BaseModel):
    """
    Used for returning refresh token data.
    """

    id: str
    user_id: str
    refresh_token: str
    expires_at: datetime
    revoked: bool

    @field_validator("id", "user_id", mode="before")
    def _normalize_ids(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v
