# auth-server/app/models/auth.py

from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict
from bson import ObjectId


class BaseMongoModel(BaseModel):
    # Pydantic v2 configuration: allow population by field name (aliases)
    model_config = ConfigDict(populate_by_name=True)


class UserCreate(BaseMongoModel):
    """Used for creating a new user."""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    hashed_password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_verified: bool = False
    last_activity_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    suspended_till: Optional[datetime] = None
    delete_at: Optional[datetime] = None


class UserId(BaseMongoModel):
    """Used for returning user data (wraps MongoDB _id)."""
    id: str = Field(..., alias="_id")

    @field_validator("id", mode="before")
    def _normalize_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v


class UserDetailed(UserId):
    """Used for returning user data with additional details."""
    username: str
    is_verified: bool
    suspended_till: Optional[datetime] = None
    delete_at: Optional[datetime] = None


class UserWithPassword(UserDetailed):
    """Used for returning user data with password."""
    hashed_password: str


class UserActivityUpdate(BaseMongoModel):
    """Used for updating user activity."""
    last_activity_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class UserPassword(BaseMongoModel):
    """Used for updating user password."""
    hashed_password: str


class UserSuspend(BaseMongoModel):
    """Used for updating user suspension."""
    suspended_till: datetime


class UserDelete(BaseMongoModel):
    """Used for updating user deletion.
      - setting for deletion
      - revoking deletion
    Actual deletion is handled by a separate cleanup process.
    """
    delete_at: Optional[datetime] = None


class UserUsername(BaseMongoModel):
    """Used for updating username."""
    username: str = Field(..., min_length=3, max_length=50)