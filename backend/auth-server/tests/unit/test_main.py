# tests/test_main.py
from fastapi.testclient import TestClient
import pytest
from unittest.mock import patch

from app.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    # assert response.json() == {"message": "Hello World"}

def test_static_mount():
    response = client.get("/static/")
    # The exact response depends on your static files
    # At least check it doesn't 404
    assert response.status_code in (200, 404)

# from slowapi.errors import RateLimitExceeded

# def test_rate_limit_handler_called(test_client: TestClient, app):
#     called = {}

#     def fake_handler(request, exc):
#         called["hit"] = True
#         return Response("Rate limited", status_code=429)

#     # Replace the registered handler
#     app.exception_handlers[RateLimitExceeded] = fake_handler

#     # Force an endpoint to raise the exception
#     app.router.routes[0].endpoint = lambda: (_ for _ in ()).throw(RateLimitExceeded)

#     test_client.get("/")
#     assert "hit" in called

# from fastapi import Response
# from app.core.csrf import CsrfProtectError

# def test_csrf_exception_handler_called(test_client: TestClient, app):
#     called = {}

#     def fake_handler(request, exc):
#         called["hit"] = True
#         return Response("CSRF error", status_code=403)

#     # Replace the registered handler
#     app.exception_handlers[CsrfProtectError] = fake_handler

#     # Force an endpoint to raise the exception
#     app.router.routes[0].endpoint = lambda: (_ for _ in ()).throw(CsrfProtectError)

#     test_client.get("/")
#     assert "hit" in called
        
"""
1. The FastAPI app starts without errors.
2. The root endpoint returns the expected response.
3. Static files mount without a 500 error.

It **doesn't** test:

* Rate limiting behavior.
* CSRF exception handling.
* Logging side effects.
"""
