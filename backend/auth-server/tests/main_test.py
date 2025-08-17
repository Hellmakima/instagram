# tests/test_main.py

# TODO: re write this to actually test the app. currently it is a dummy test.

import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


def test_app_starts(client: TestClient):
    # sanity check: app responds at all
    response = client.get("/")
    assert response.status_code in [200, 404]


def test_router_included(client: TestClient):
    # adjust path to one you actually have in router
    response = client.get("/api/v1/auth/")
    assert response.status_code in [200, 404]


def test_static_files(client: TestClient):
    response = client.get("/static/")
    assert response.status_code in [200, 404]


def test_rate_limit_handler_exists():
    # just check handler is registered
    handlers = app.exception_handlers
    assert any("RateLimitExceeded" in str(h) for h in handlers.values())


def test_csrf_handler_exists():
    handlers = app.exception_handlers
    assert any("CsrfProtectError" in str(h) for h in handlers.values())
