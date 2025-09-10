# tests/unit/conftest.py

import pytest

import pytest
from unittest.mock import AsyncMock, Mock

@pytest.fixture
def mock_db_client():
    """Provides a mock database client for unit tests."""
    mock_collection = AsyncMock()
    mock_collection.insert_one.return_value.inserted_id = "fake_id_123"
    
    mock_db = Mock()
    mock_db.get_collection.return_value = mock_collection
    return mock_db

