# tests/conftest.py
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from app.main import app as fastapi_app
from app.core.config import settings
from .mongo_client import MongoClient

"""
# TODO: setup test DB
@pytest_asyncio.fixture()
def env_setup():
    os.environ["MONGODB_DBNAME"] = os.environ.get("TEST_DB_NAME")
    os.environ["MONGODB_URL"] = os.environ.get("TEST_MONGODB_URL")
# use:
@pytest_asyncio.fixture()
def test_client(env_setup):
"""


import pytest
from fastapi.testclient import TestClient
import pytest
from app.main import app as fastapi_app

@pytest.fixture()
def app():
    return fastapi_app


@pytest.fixture()
def test_client():
    with TestClient(fastapi_app) as client:
        yield client


@pytest_asyncio.fixture()
async def mongo_client():
    print('\033[92mSetting test db\033[0m')
    async with MongoClient(
        settings.MONGODB_DBNAME,
        # os.environ.get("TEST_DB_NAME"),
        'users'
    ) as mongo_client:
        yield mongo_client