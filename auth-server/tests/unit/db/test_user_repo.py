# tests/unit/db/test_user_repo.py
import pytest
from app.db.repositories.user_repo import UserRepository
from unittest.mock import AsyncMock, Mock


@pytest.mark.asyncio
async def test_find_by_username_or_email_found(
    mock_db_client: Mock,
    mock_db_collection: AsyncMock
):
    """Tests that find_by_username_or_email returns a user if found."""
    # Define the mock return value for the find_one method
    mock_user_data = {
        "_id": "60a123456789abcdef0123456",
        "hashed_password": "hashed_password_string",
        "is_deleted": False,
        "is_blocked": False,
        "is_verified": True,
    }
    mock_db_collection.find_one.return_value = mock_user_data

    # Instantiate the repository with the mock client
    repo = UserRepository(db=mock_db_client)

    # Call the method under test
    user = await repo.find_by_username_or_email(identifier="testuser")

    # Assertions:
    # 1. The method returned the expected data.
    assert user == mock_user_data
    # 2. The underlying database method was called with the correct arguments.
    mock_db_collection.find_one.assert_called_once_with(
        {"$or": [{"username": "testuser"}, {"email": "testuser"}]},
        projection={
            "_id": 1,
            "hashed_password": 1,
            "is_deleted": 1,
            "is_blocked": 1,
            "is_verified": 1,
        },
    )


@pytest.mark.asyncio
async def test_find_by_username_or_email_not_found(
    mock_db_client: Mock,
    mock_db_collection: AsyncMock
):
    """Tests that find_by_username_or_email returns None if no user is found."""
    # Mock find_one to return None, simulating no user found
    mock_db_collection.find_one.return_value = None

    # Instantiate the repository with the mock client
    repo = UserRepository(db=mock_db_client)

    # Call the method under test
    user = await repo.find_by_username_or_email(identifier="nonexistent_user")

    # Assertions:
    assert user is None
    mock_db_collection.find_one.assert_called_once()