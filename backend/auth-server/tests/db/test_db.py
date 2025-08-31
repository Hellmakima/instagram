# tests/db/test_db.py
import pytest
from unittest.mock import MagicMock # helps create mock objects
from app.db.db import get_db, get_client
from app.core.config import settings

@pytest.mark.asyncio # asyncio is required for get_db
async def test_get_db_simple():
    fake_client = {settings.MONGODB_DBNAME: "fake_db"}          # pretend DB
    fake_request = MagicMock()
    fake_request.app.state.client = fake_client

    db = await get_db(fake_request)
    assert db == "fake_db"                     # ensures get_db returns what we expect

@pytest.mark.asyncio
async def test_get_client_simple():
    fake_client = "my_fake_client"
    fake_request = MagicMock()
    fake_request.app.state.client = fake_client

    client = await get_client(fake_request)
    assert client == fake_client
