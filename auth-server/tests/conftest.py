# tests/conftest.py

import pytest
from app.main import app as fastapi_app


@pytest.fixture(scope="session")
def app():
    return fastapi_app

