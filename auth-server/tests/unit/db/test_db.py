# tests/unit/db/test_db.py

import pytest
from unittest.mock import MagicMock, AsyncMock

from app.db import db
from app.core.config import settings


@pytest.fixture
def mock_motor_client():
    """
    Returns a mocked AsyncIOMotorClient with database and collection mocks
    """
    client = MagicMock()
    db = AsyncMock()
    client.get_database.return_value = db
    client.admin.command = AsyncMock()
    db.__getitem__.return_value = AsyncMock()
    return client


@pytest.mark.asyncio
async def test_get_db_returns_correct_database(mock_request, mock_motor_client):
    # Assign the mocked client to request
    mock_request.app.state.client = mock_motor_client

    result = await db.get_db(mock_request)

    # Ensure it returned the database corresponding to settings.MONGODB_DBNAME
    mock_motor_client.__getitem__.assert_called_once_with(settings.MONGODB_DBNAME)
    assert result == mock_motor_client.__getitem__.return_value


@pytest.mark.asyncio
async def test_get_client_returns_client(mock_request, mock_motor_client):
    mock_request.app.state.client = mock_motor_client

    result = await db.get_client(mock_request)

    assert result == mock_motor_client
