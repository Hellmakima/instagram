# File: auth-server/tests/unit/db/repositories/test_refresh_token.py

import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime, timezone, timedelta

from app.repositories import refresh_token as refresh_token_repo
from app.core.config import settings


@pytest.mark.asyncio
async def test_find_by_token_calls_collection_correctly():
    # Arrange
    mock_collection = AsyncMock()
    mock_collection.find_one = AsyncMock(return_value={"_id": "abc", "user_id": "user123"})
    mock_db = MagicMock()
    mock_db.get_collection.return_value = mock_collection

    repo = refresh_token_repo.RefreshToken(mock_db)
    token = "token123"

    # Act
    result = await repo.find_by_token(token)

    # Assert
    mock_collection.find_one.assert_awaited_once_with(
        {"refresh_token": token, "revoked": False},
        projection={"_id": 1, "user_id": 1, "expires_at": 1, "revoked": 1},
    )
    assert result == {"_id": "abc", "user_id": "user123"}


@pytest.mark.asyncio
async def test_insert_calls_collection_with_correct_doc():
    mock_collection = AsyncMock()
    mock_collection.insert_one = AsyncMock(return_value="inserted")
    mock_db = MagicMock()
    mock_db.get_collection.return_value = mock_collection

    repo = refresh_token_repo.RefreshToken(mock_db)
    user_id = "user123"
    token = "token123"

    result = await repo.insert(user_id, token)

    assert mock_collection.insert_one.await_count == 1
    inserted_doc = mock_collection.insert_one.call_args[0][0]

    # Check fields
    assert inserted_doc["user_id"] == user_id
    assert inserted_doc["refresh_token"] == token
    assert inserted_doc["revoked"] is False
    assert isinstance(inserted_doc["expires_at"], datetime)
    assert result == "inserted"


@pytest.mark.asyncio
async def test_delete_by_token_calls_delete_one():
    mock_collection = AsyncMock()
    mock_collection.delete_one = AsyncMock(return_value="deleted")
    mock_db = MagicMock()
    mock_db.get_collection.return_value = mock_collection

    repo = refresh_token_repo.RefreshToken(mock_db)
    token = "token123"

    result = await repo.delete_by_token(token)

    mock_collection.delete_one.assert_awaited_once_with({"refresh_token": token})
    assert result == "deleted"


@pytest.mark.asyncio
async def test_revoke_calls_update_one_correctly():
    mock_collection = AsyncMock()
    mock_collection.update_one = AsyncMock(return_value="updated")
    mock_db = MagicMock()
    mock_db.get_collection.return_value = mock_collection

    repo = refresh_token_repo.RefreshToken(mock_db)
    token_id = "tokenid123"

    result = await repo.revoke(token_id)

    mock_collection.update_one.assert_awaited_once_with(
        {"_id": token_id}, {"$set": {"revoked": True}}, session=None
    )
    assert result == "updated"
