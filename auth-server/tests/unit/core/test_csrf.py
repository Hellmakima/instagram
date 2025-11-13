# auth-server/tests/unit/core/test_csrf.py
import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi_csrf_protect.exceptions import CsrfProtectError

from app.core import csrf


@pytest.mark.asyncio
async def test_verify_csrf_success(mock_request, mock_response, mock_csrf):
    mock_csrf.validate_csrf = AsyncMock()
    mock_csrf.unset_csrf_cookie = MagicMock()

    await csrf.verify_csrf(mock_request, mock_response, csrf_protect=mock_csrf)

    mock_csrf.validate_csrf.assert_awaited_once_with(mock_request)
    mock_csrf.unset_csrf_cookie.assert_called_once_with(mock_response)


@pytest.mark.asyncio
async def test_verify_csrf_failure(mock_request, mock_response, mock_csrf):
    mock_csrf.validate_csrf = AsyncMock(
        side_effect=CsrfProtectError(status_code=403, message="CSRF validation failed")
    )
    mock_csrf.unset_csrf_cookie = AsyncMock()

    with pytest.raises(CsrfProtectError):
        await csrf.verify_csrf(mock_request, mock_response, csrf_protect=mock_csrf)

    mock_csrf.unset_csrf_cookie.assert_not_called()


def test_csrf_exception_handler_returns_json(mock_request):
    exc = CsrfProtectError(status_code=403, message="CSRF validation failed")

    response = csrf.csrf_exception_handler(mock_request, exc)

    assert response.status_code == 403
    content = bytes(response.body).decode()
    assert "CSRF validation failed" in content
    assert "CSRF_INVALID_TOKEN" in content


def test_csrf_exception_handler_raises_for_non_csrf(mock_request):
    exc = ValueError("something else")
    with pytest.raises(ValueError):
        csrf.csrf_exception_handler(mock_request, exc)
