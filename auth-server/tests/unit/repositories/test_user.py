# tests/unit/repositories/test_user.py

import pytest
from unittest.mock import AsyncMock, MagicMock
from bson import ObjectId

from app.repositories import user
from app.models.auth import User as UserModel, UserOut
from datetime import datetime, timezone, timedelta


@pytest.mark.asyncio
async def test_get_by_username_or_email_returns_user():
    mock_collection = AsyncMock()
    fake_id = ObjectId()
    mock_collection.find_one.return_value = {
        "_id": fake_id,
        "hashed_password": "hashed",
        "is_pending_deletion": False,
        "is_suspended": False,
        "is_verified": True,
    }

    repo = user.User(db=MagicMock())
    repo.collection = mock_collection

    result: UserOut | None = await repo.get_by_username_or_email("test")

    assert result is not None

    mock_collection.find_one.assert_called_once()
    assert result.id == str(fake_id)
    assert result.hashed_password == "hashed"
    assert result.is_verified is True

@pytest.mark.asyncio
async def test_get_by_username_or_email_returns_none():
    mock_collection = AsyncMock()
    mock_collection.find_one.return_value = None

    repo = user.User(db=MagicMock())
    repo.collection = mock_collection

    result = await repo.get_by_username_or_email("notfound")
    assert result is None

@pytest.mark.asyncio
async def test_get_verified_returns_record():
    mock_collection = AsyncMock()
    fake_record = {"_id": ObjectId()}
    mock_collection.find_one.return_value = fake_record

    repo = user.User(db=MagicMock())
    repo.collection = mock_collection

    result = await repo.get_verified("user", "email@example.com")
    mock_collection.find_one.assert_called_once()
    assert result == fake_record

@pytest.mark.asyncio
async def test_get_verified_returns_none():
    mock_collection = AsyncMock()
    mock_collection.find_one.return_value = None

    repo = user.User(db=MagicMock())
    repo.collection = mock_collection

    result = await repo.get_verified("user", "email@example.com")
    assert result is None

@pytest.mark.asyncio
async def test_create_user_inserts_document():
    mock_collection = AsyncMock()
    inserted_id = ObjectId()
    mock_collection.insert_one.return_value.inserted_id = inserted_id

    repo = user.User(db=MagicMock())
    repo.collection = mock_collection

    user_doc = UserModel(
        username="test",
        email="test@example.com",
        hashed_password="hashed",
        created_at=datetime.now(timezone.utc),
        is_verified=True,
        is_suspended=False,
        suspended_till=None,
        last_activity_at=datetime.now(timezone.utc),
        is_pending_deletion=False,
        delete_at=datetime.now(timezone.utc) + timedelta(hours=6),
    )

    result = await repo.create(user_doc)
    mock_collection.insert_one.assert_called_once()
    assert result == inserted_id

@pytest.mark.asyncio
async def test_get_by_username_or_email_raises_exception():
    mock_collection = AsyncMock()
    mock_collection.find_one.side_effect = Exception("DB failure")

    repo = user.User(db=MagicMock())
    repo.collection = mock_collection

    with pytest.raises(Exception, match="DB failure"):
        await repo.get_by_username_or_email("testuser")


@pytest.mark.asyncio
async def test_get_verified_raises_exception():
    mock_collection = AsyncMock()
    mock_collection.find_one.side_effect = Exception("boom")

    repo = user.User(db=MagicMock())
    repo.collection = mock_collection

    with pytest.raises(Exception, match="boom"):
        await repo.get_verified("u", "e@mail.com")


@pytest.mark.asyncio
async def test_create_raises_exception():
    mock_collection = AsyncMock()
    mock_collection.insert_one.side_effect = Exception("insert fail")

    repo = user.User(db=MagicMock())
    repo.collection = mock_collection

    user_doc = MagicMock()
    user_doc.model_dump.return_value = {"fake": "data"}

    with pytest.raises(Exception, match="insert fail"):
        await repo.create(user_doc)

    user_doc.model_dump.assert_called_once()
