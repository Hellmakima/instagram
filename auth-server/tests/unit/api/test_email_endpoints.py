from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch


def test_send_verification_email_endpoint_calls_service(app):
    # Patch the send_verification_email service to avoid real email work
    mock_send = AsyncMock(return_value=True)
    # get_user_repo is a dependency; provide a simple callable that returns a dummy repo

    with patch(
        "app.api.api_v1.endpoints.email.router.send_verification_email_service",
        new=mock_send,
    ):
        # Override the get_user_repo dependency to avoid DB access
        from app.api.dependencies.db_deps import get_user_repo

        original = app.dependency_overrides.get(get_user_repo)
        app.dependency_overrides[get_user_repo] = lambda db=None: object()
        try:
            with TestClient(app) as client:
                # We need a CSRF token first (the static pages do this during real flow)
                r = client.get("/v1/auth/csrf-token")
                assert r.status_code == 200
                csrf = r.json()["data"]["csrf_token"]

                # Call the endpoint (user_id and email are arbitrary strings)
                resp = client.get(
                    f"/v1/email/send-verification-email?user_id=testid&email=test@gmail.com",
                    headers={"X-CSRF-Token": csrf},
                )
                assert resp.status_code == 200
                body = resp.json()
                # The endpoint returns a JSON with ok flag
                assert "ok" in body
                # Ensure our service mock was awaited
                assert mock_send.await_count >= 1
        finally:
            # restore override
            if original is None:
                app.dependency_overrides.pop(get_user_repo, None)
            else:
                app.dependency_overrides[get_user_repo] = original


def test_verify_email_endpoint_calls_service(app):
    # Patch the verify service
    mock_verify = AsyncMock(return_value="user123")
    with patch(
        "app.api.api_v1.endpoints.email.router.verify_email_token_service",
        new=mock_verify,
    ):
        from app.api.dependencies.db_deps import get_user_repo

        original = app.dependency_overrides.get(get_user_repo)
        app.dependency_overrides[get_user_repo] = lambda db=None: object()
        try:
            with TestClient(app) as client:
                resp = client.get("/v1/email/verify-email?token=abc")
                assert resp.status_code == 200
                body = resp.json()
                assert body.get("ok") is True
                assert body.get("user_id") == "user123"
                assert mock_verify.await_count >= 1
        finally:
            if original is None:
                app.dependency_overrides.pop(get_user_repo, None)
            else:
                app.dependency_overrides[get_user_repo] = original
