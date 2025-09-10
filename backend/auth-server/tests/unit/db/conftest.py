# tests/unit/db/conftest.py

import pytest
from unittest.mock import AsyncMock, Mock

@pytest.fixture
def mock_db_collection(mocker: Mock):
    """Provides a mocked MongoDB collection object."""
    mock_collection = mocker.AsyncMock()
    return mock_collection

@pytest.fixture
def mock_db_client(mocker: Mock, mock_db_collection: AsyncMock):
    """Provides a mocked MongoDB database client."""
    mock_client = mocker.Mock()
    mock_client.get_collection.return_value = mock_db_collection
    return mock_client