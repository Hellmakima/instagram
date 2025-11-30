# tests/unit/conftest.py
# TODO: distribute fixtures to relevant folders.

import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import Request, Response


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
