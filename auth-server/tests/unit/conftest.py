# tests/unit/conftest.py
# TODO: distribute fixtures to relevant folders.

import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import Request, Response

@pytest.fixture
def mock_db_client():
    """Provides a mock database client for unit tests."""
    mock_collection = AsyncMock()
    mock_collection.insert_one.return_value.inserted_id = "fake_id_123"

    mock_db = MagicMock()
    mock_db.__getitem__.return_value = mock_collection  # for db[collection_name]
    return mock_db

@pytest.fixture
def mock_db_collection():
    """Mocked database collection for Mongo operations."""
    collection = AsyncMock()
    collection.insert_one.return_value.inserted_id = "fake_id_123"
    collection.find_one.return_value = {"_id": "fake_id_123", "username": "testuser"}
    collection.update_one.return_value.modified_count = 1
    return collection

@pytest.fixture
def mock_request():
    """Mocked FastAPI Request object."""
    return MagicMock(spec=Request)

@pytest.fixture
def mock_response():
    """Mocked FastAPI Response object."""
    return MagicMock(spec=Response)

@pytest.fixture
def mock_csrf():
    """Mocked csrf_protect object for verify_csrf tests."""
    csrf_mock = AsyncMock()
    csrf_mock.validate_csrf = AsyncMock()
    csrf_mock.unset_csrf_cookie = AsyncMock()
    return csrf_mock
