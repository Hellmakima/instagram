# File: auth-server/tests/unit/db/repositories/test_refresh_token.py

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timezone, timedelta
from app.repositories import refresh_token as refresh_token_repo

# --- Fixtures and Mocks ---
# Note: For production, settings.REFRESH_TOKEN_EXPIRE_MINUTES should be mocked here too.
# Assuming a setting of 10 minutes for this example.
EXPIRE_MINUTES = 10 
MOCKED_NOW = datetime(2025, 10, 16, 8, 37, 12, 529748, tzinfo=timezone.utc)
MOCKED_EXPIRY = MOCKED_NOW + timedelta(minutes=EXPIRE_MINUTES)

@pytest.fixture
def mock_refresh_token_collection():
    collection = AsyncMock()
    collection.insert_one.return_value.inserted_id = "fake_id_123"
    collection.update_one.return_value.modified_count = 1
    return collection

@pytest.fixture
def mock_refresh_token_db(mock_refresh_token_collection):
    mock_db = MagicMock()
    mock_db.get_collection.return_value = mock_refresh_token_collection
    return mock_db

# --- Test Cases ---

@pytest.mark.asyncio
@patch('app.repositories.refresh_token.datetime', MagicMock(now=MagicMock(return_value=MOCKED_NOW)))
async def test_find_by_token_calls_collection_correctly(mock_refresh_token_db, mock_refresh_token_collection):
    """Tests the success path, including the new expiration check in the filter."""
    repo = refresh_token_repo.RefreshToken(mock_refresh_token_db)
    token = "token123"

    mock_refresh_token_collection.find_one = AsyncMock(return_value={"_id": "abc", "user_id": "user123"})

    result = await repo.find_by_token("token123")

    mock_refresh_token_collection.find_one.assert_awaited_once_with(
        {
            "refresh_token": token, 
            "revoked": False,
            "expires_at": {"$gt": MOCKED_NOW},
        },
        projection={"_id": 1, "user_id": 1, "expires_at": 1, "revoked": 1},
    )
    assert result is not None

@pytest.mark.asyncio
@patch('app.repositories.refresh_token.datetime', MagicMock(now=MagicMock(return_value=MOCKED_NOW)))
async def test_insert_calls_collection_with_correct_doc(mock_refresh_token_db, mock_refresh_token_collection):
    """Verifies all fields, especially deterministic expires_at, are set on insert."""
    repo = refresh_token_repo.RefreshToken(mock_refresh_token_db)
    user_id = "user123"
    token = "token123"
    
    # Mock settings for deterministic calculation
    with patch('app.repositories.refresh_token.settings') as mock_settings:
        mock_settings.REFRESH_TOKEN_EXPIRE_MINUTES = EXPIRE_MINUTES
        mock_refresh_token_collection.insert_one = AsyncMock(return_value="inserted")

        result = await repo.insert(user_id, token)

    mock_refresh_token_collection.insert_one.assert_awaited_once()

    inserted_doc = mock_refresh_token_collection.insert_one.call_args[0][0]
    assert inserted_doc["user_id"] == user_id
    assert inserted_doc["refresh_token"] == token
    assert inserted_doc["revoked"] is False
    # CORRECT ASSERTION: Check the exact calculated expiration time
    assert inserted_doc["expires_at"] == MOCKED_EXPIRY
    assert result == "inserted"


@pytest.mark.asyncio
async def test_delete_by_token_calls_delete_one(mock_refresh_token_db, mock_refresh_token_collection):
    """Tests the delete-by-token functionality (though revocation is preferred)."""
    repo = refresh_token_repo.RefreshToken(mock_refresh_token_db)
    token = "token123"

    mock_refresh_token_collection.delete_one = AsyncMock(return_value="deleted")

    result = await repo.delete_by_token(token)

    mock_refresh_token_collection.delete_one.assert_awaited_once_with({"refresh_token": token})
    assert result == "deleted"


@pytest.mark.asyncio
async def test_revoke_calls_update_one_correctly(mock_refresh_token_db, mock_refresh_token_collection):
    """Tests the basic revocation query via token ID."""
    repo = refresh_token_repo.RefreshToken(mock_refresh_token_db)
    token_id = "tokenid123"

    mock_refresh_token_collection.update_one = AsyncMock(return_value="updated")

    result = await repo.revoke(token_id)

    mock_refresh_token_collection.update_one.assert_awaited_once_with(
        {"_id": token_id}, {"$set": {"revoked": True}}, session=None
    )
    assert result == "updated"


# --- Security-Critical Negative Tests ---

@pytest.mark.asyncio
@patch('app.repositories.refresh_token.datetime', MagicMock(now=MagicMock(return_value=MOCKED_NOW)))
async def test_find_by_token_rejects_revoked_token(mock_refresh_token_db, mock_refresh_token_collection):
    repo = refresh_token_repo.RefreshToken(mock_refresh_token_db)
    token = "token123"

    # CRITICAL FIX: The mock must return None to simulate the DB rejecting the token due to the "revoked": False filter.
    mock_refresh_token_collection.find_one = AsyncMock(return_value=None) 

    result = await repo.find_by_token(token)

    # Assert the secure query was sent (correct)
    mock_refresh_token_collection.find_one.assert_awaited_once_with(
        {
            "refresh_token": token,
            "revoked": False, 
            "expires_at": {"$gt": MOCKED_NOW},
        },
        projection={"_id": 1, "user_id": 1, "expires_at": 1, "revoked": 1},
    )
    # Assert the result is None (now correct)
    assert result is None

@pytest.mark.asyncio
@patch('app.repositories.refresh_token.datetime', MagicMock(now=MagicMock(return_value=MOCKED_NOW)))
async def test_find_by_token_rejects_expired_token(mock_refresh_token_db, mock_refresh_token_collection):
    repo = refresh_token_repo.RefreshToken(mock_refresh_token_db)
    token = "expired_token"

    # No need to calculate expired_time, just set the mock result to None
    # CRITICAL FIX: The mock must return None to simulate the DB rejecting the token due to the expiration filter.
    mock_refresh_token_collection.find_one = AsyncMock(return_value=None)

    result = await repo.find_by_token(token)

    # Assert the secure query was sent (correct)
    mock_refresh_token_collection.find_one.assert_awaited_once_with(
        {
            "refresh_token": token,
            "revoked": False,
            "expires_at": {"$gt": MOCKED_NOW},
        },
        projection={"_id": 1, "user_id": 1, "expires_at": 1, "revoked": 1},
    )
    # Assert the result is None (now correct)
    assert result is None