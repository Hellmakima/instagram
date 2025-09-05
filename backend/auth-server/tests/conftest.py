# tests/conftest.py

import os
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from dotenv import load_dotenv
from app.main import app as fastapi_app
from .mongo_client import MongoClient

load_dotenv(dotenv_path=".env.test", override=True)

@pytest.fixture(scope="session", autouse=True)
def env_setup():
    os.environ.setdefault("MONGODB_DBNAME", "instagram_test")
    os.environ.setdefault("MONGODB_URL", "mongodb://localhost:27017/instagram_test")


@pytest.fixture(scope="session")
def app():
    return fastapi_app


@pytest.fixture()
def test_client(app, env_setup):
    with TestClient(app) as client:
        yield client


@pytest_asyncio.fixture()
async def mongo_client(env_setup):
    print("\033[92mSetting test db\033[0m")
    async with MongoClient(
        os.environ["MONGODB_DBNAME"],
        "users"
    ) as mongo:
        yield mongo
        await mongo.db["users"].delete_many({})
        await mongo.db["refresh_tokens"].delete_many({})
