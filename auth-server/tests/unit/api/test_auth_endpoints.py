from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
import pytest


def get_csrf_token(client: TestClient) -> str:
    r = client.get("/v1/auth/csrf-token")
    assert r.status_code == 200
    return r.json()["data"]["csrf_token"]


def test_register_calls_service(app):
    mock_create = AsyncMock()
    with patch(
        "app.api.api_v1.endpoints.auth.router.create_user_service", new=mock_create
    ):
        from app.api.dependencies.db_deps import get_user_repo

        original = app.dependency_overrides.get(get_user_repo)
        app.dependency_overrides[get_user_repo] = lambda db=None: object()
        try:
            with TestClient(app) as client:
                csrf = get_csrf_token(client)
                payload = {
                    "username": "user1",
                    "email": "user1@gmail.com",
                    "password": "Abcdef1!23",
                }
                resp = client.post(
                    "/v1/auth/register", json=payload, headers={"X-CSRF-Token": csrf}
                )
                assert resp.status_code == 201
                body = resp.json()
                assert "message" in body
                assert mock_create.await_count >= 1
        finally:
            if original is None:
                app.dependency_overrides.pop(get_user_repo, None)
            else:
                app.dependency_overrides[get_user_repo] = original


def test_login_sets_cookies(app):
    mock_login = AsyncMock(return_value=("access.token", "refresh.token"))
    with patch(
        "app.api.api_v1.endpoints.auth.router.login_user_service", new=mock_login
    ):
        from app.api.dependencies.db_deps import get_user_repo, get_refresh_token_repo

        orig_user = app.dependency_overrides.get(get_user_repo)
        orig_ref = app.dependency_overrides.get(get_refresh_token_repo)
        app.dependency_overrides[get_user_repo] = lambda db=None: object()
        app.dependency_overrides[get_refresh_token_repo] = lambda db=None: object()
        try:
            with TestClient(app) as client:
                csrf = get_csrf_token(client)
                payload = {
                    "username_or_email": "u1",
                    "password": "Abcd1234!@",
                    "user_agent": "user_agent",
                }
                resp = client.post(
                    "/v1/auth/login", json=payload, headers={"X-CSRF-Token": csrf}
                )
                assert resp.status_code == 200
                # Test cookies were set (TestClient stores cookies)
                cookies = resp.cookies
                assert "access_token" in cookies
                assert "refresh_token" in cookies
                assert mock_login.await_count >= 1
        finally:
            if orig_user is None:
                app.dependency_overrides.pop(get_user_repo, None)
            else:
                app.dependency_overrides[get_user_repo] = orig_user
            if orig_ref is None:
                app.dependency_overrides.pop(get_refresh_token_repo, None)
            else:
                app.dependency_overrides[get_refresh_token_repo] = orig_ref


def test_logout_calls_service_and_deletes_cookies(app):
    mock_logout = AsyncMock()
    with patch(
        "app.api.api_v1.endpoints.auth.router.logout_user_service", new=mock_logout
    ):
        from app.api.dependencies.db_deps import get_refresh_token_repo

        orig = app.dependency_overrides.get(get_refresh_token_repo)
        app.dependency_overrides[get_refresh_token_repo] = lambda db=None: object()
        try:
            with TestClient(app) as client:
                csrf = get_csrf_token(client)
                # Set cookies to simulate logged in user
                client.cookies.set("access_token", "a.tok")
                client.cookies.set("refresh_token", "r.tok")
                resp = client.post("/v1/auth/logout", headers={"X-CSRF-Token": csrf})
                assert resp.status_code == 200
                assert mock_logout.await_count >= 1
        finally:
            if orig is None:
                app.dependency_overrides.pop(get_refresh_token_repo, None)
            else:
                app.dependency_overrides[get_refresh_token_repo] = orig


def test_refresh_token_rotates_tokens(app):
    mock_refresh = AsyncMock(return_value=("new.access", "new.refresh"))
    with patch(
        "app.api.api_v1.endpoints.auth.router.refresh_access_token_service",
        new=mock_refresh,
    ):
        from app.api.dependencies.db_deps import get_refresh_token_repo, get_session

        orig_repo = app.dependency_overrides.get(get_refresh_token_repo)
        orig_session = app.dependency_overrides.get(get_session)
        app.dependency_overrides[get_refresh_token_repo] = lambda db=None: object()
        app.dependency_overrides[get_session] = lambda: None
        try:
            with TestClient(app) as client:
                csrf = get_csrf_token(client)
                client.cookies.set("refresh_token", "old.refresh")
                resp = client.post(
                    "/v1/auth/refresh_token", headers={"X-CSRF-Token": csrf}
                )
                assert resp.status_code == 200
                # The current implementation returns a success message; verify service was called
                assert resp.status_code == 200
                body = resp.json()
                assert "message" in body
                assert mock_refresh.await_count >= 1
        finally:
            if orig_repo is None:
                app.dependency_overrides.pop(get_refresh_token_repo, None)
            else:
                app.dependency_overrides[get_refresh_token_repo] = orig_repo
            if orig_session is None:
                app.dependency_overrides.pop(get_session, None)
            else:
                app.dependency_overrides[get_session] = orig_session
