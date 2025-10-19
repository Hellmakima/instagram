# tests/unit/repositories/test_user.py

import pytest
from unittest.mock import AsyncMock, MagicMock
from bson import ObjectId
from datetime import datetime, timezone, timedelta

from app.repositories import user
from app.models.auth import UserCreate as UserModel, UserWithPassword as UserOut

# Fixtures for user repo tests
@pytest.fixture
def mock_user_collection():
    """Provides a mock MongoDB collection for the User repo."""
    collection = AsyncMock()
    return collection

@pytest.fixture
def mock_user_db(mock_user_collection):
    """Provides a mock DB client with get_collection returning the mock collection."""
    mock_db = MagicMock()
    mock_db.get_collection.return_value = mock_user_collection
    return mock_db


@pytest.mark.asyncio
async def test_get_by_username_or_email_returns_user(mock_user_db, mock_user_collection):
    # Arrange: setup collection to return a fake user
    fake_id = ObjectId()
    mock_user_collection.find_one.return_value = {
        "_id": fake_id,
        "username": "test",
        "hashed_password": "hashed",
        "delete_at": None,
        "suspended_till": None,
        "is_verified": True,
    }

    repo = user.User(db=mock_user_db)

    # Act
    result: UserOut | None = await repo.get_by_username_or_email("test")

    # Assert
    assert result is not None
    mock_user_collection.find_one.assert_called_once()
    assert str(result.id) == str(fake_id)
    assert result.hashed_password == "hashed"
    assert result.is_verified is True


@pytest.mark.asyncio
async def test_get_by_username_or_email_returns_none(mock_user_db, mock_user_collection):
    mock_user_collection.find_one.return_value = None

    repo = user.User(db=mock_user_db)
    result = await repo.get_by_username_or_email("notfound")
    assert result is None


@pytest.mark.asyncio
async def test_get_verified_returns_record(mock_user_db, mock_user_collection):
    fake_record = {"_id": ObjectId()}
    mock_user_collection.find_one.return_value = fake_record

    repo = user.User(db=mock_user_db)
    result = await repo.get_verified("user", "email@example.com")

    mock_user_collection.find_one.assert_called_once()
    assert result == fake_record


@pytest.mark.asyncio
async def test_get_verified_returns_none(mock_user_db, mock_user_collection):
    mock_user_collection.find_one.return_value = None

    repo = user.User(db=mock_user_db)
    result = await repo.get_verified("user", "email@example.com")
    assert result is None


@pytest.mark.asyncio
async def test_create_user_inserts_document(mock_user_db, mock_user_collection):
    inserted_id = ObjectId()
    mock_user_collection.insert_one.return_value.inserted_id = inserted_id

    repo = user.User(db=mock_user_db)

    user_doc = UserModel(
        username="test",
        email="test@example.com",
        hashed_password="hashed",
        created_at=datetime.now(timezone.utc),
        is_verified=True,
        last_activity_at=datetime.now(timezone.utc),
        suspended_till=None,
        delete_at=datetime.now(timezone.utc) + timedelta(hours=6),
    )

    result = await repo.create(user_doc)

    mock_user_collection.insert_one.assert_called_once()
    # repo.create now returns a string id
    assert isinstance(result, str)


@pytest.mark.asyncio
async def test_get_by_username_or_email_raises_exception(mock_user_db, mock_user_collection):
    mock_user_collection.find_one.side_effect = Exception("DB failure")

    repo = user.User(db=mock_user_db)

    with pytest.raises(Exception, match="DB failure"):
        await repo.get_by_username_or_email("testuser")


@pytest.mark.asyncio
async def test_get_verified_raises_exception(mock_user_db, mock_user_collection):
    mock_user_collection.find_one.side_effect = Exception("boom")

    repo = user.User(db=mock_user_db)

    with pytest.raises(Exception, match="boom"):
        await repo.get_verified("u", "e@mail.com")


@pytest.mark.asyncio
async def test_create_raises_exception(mock_user_db, mock_user_collection):
    mock_user_collection.insert_one.side_effect = Exception("insert fail")

    repo = user.User(db=mock_user_db)

    user_doc = MagicMock()
    user_doc.model_dump.return_value = {"fake": "data"}

    with pytest.raises(Exception, match="insert fail"):
        await repo.create(user_doc)

    user_doc.model_dump.assert_called_once()
