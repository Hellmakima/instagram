from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, Any
from app.models.auth import (
    UserCreate as UserCreateModel,
    UserDetailed as UserDetailedModel,
    UserWithPassword as UserWithPasswordModel,
    UserId as UserIdModel,
)

from app.models.refresh_token import (
    RefreshTokenCreate as RefreshTokenCreateModel,
    RefreshTokenOut as RefreshTokenOutModel,
)


class UserRepositoryInterface(ABC):
    @abstractmethod
    async def create(self, user_doc: UserCreateModel) -> str:
        """Create a new user and return the created id as string."""

    @abstractmethod
    async def get_by_username_or_email(self, identifier: str) -> Optional[UserWithPasswordModel]:
        """Get a user by username or email."""

    @abstractmethod
    async def get_verified(self, username: str, email: str) -> Optional[UserDetailedModel]:
        """Return a record if username/email exists and is verified."""

    @abstractmethod
    async def get_by_id(self, user_id: str) -> Optional[UserDetailedModel]:
        """Get user by id."""

    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[UserIdModel]:
        """Get user id by username."""

    @abstractmethod
    async def mark_as_verified(self, user_id: str) -> bool:
        """Mark the user as verified. Returns True if updated."""


class RefreshTokenRepositoryInterface(ABC):
    @abstractmethod
    async def insert(self, user_id: str, refresh_token: str, user_agent: str, session: Any = None) -> None:
        """Insert a refresh token record."""

    @abstractmethod
    async def find_by_token(self, token: str) -> Optional[RefreshTokenOutModel]:
        """Find a refresh token record by token string."""

    @abstractmethod
    async def revoke(self, token_id: Any, session: Any = None) -> None:
        """Revoke a refresh token by id."""

    @abstractmethod
    async def delete_by_token(self, token: str) -> None:
        """Delete a refresh token document by token string."""
