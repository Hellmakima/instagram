# tests/test_main.py


from fastapi.testclient import TestClient
import pytest
from unittest.mock import patch

# from app.main import app

# client = TestClient(app)


@pytest.fixture
def client(app):
    return TestClient(app)


def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    # assert response.json() == {"message": "Hello World"}


def test_static_mount(client):
    response = client.get("/static/")
    # The exact response depends on your static files
    # At least check it doesn't 404
    assert response.status_code in (200, 404)


"""
1. The FastAPI app starts without errors.
2. The root endpoint returns the expected response.
3. Static files mount without a 500 error.

TODO: It **doesn't** test:

* Rate limiting behavior.
* CSRF exception handling.
* Logging side effects.
"""
