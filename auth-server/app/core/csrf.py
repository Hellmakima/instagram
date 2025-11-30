# app/core/csrf.py

from fastapi import Response, Depends, Request, status
from fastapi.responses import JSONResponse
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError
from pydantic_settings import BaseSettings
from app.core.config import settings

import logging

security_logger = logging.getLogger("security_logger")
flow_logger = logging.getLogger("app_flow")


# TODO: rewrite this
class CsrfSettings(BaseSettings):
    secret_key: str | None = settings.CSRF_SECRET_KEY
    cookie_samesite: str = "lax"
    cookie_secure: bool = False  # HTTPS only
    header_name: str = "X-CSRF-Token"


@CsrfProtect.load_config
def get_csrf_config():
    return CsrfSettings()


def csrf_exception_handler(request: Request, exc: Exception):
    # FastAPI exception handlers receive (request, exc)
    if not isinstance(exc, CsrfProtectError):
        raise exc  # re-raise if not the expected exception

    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={
            "success": False,
            "message": "CSRF validation failed",
            "error": {
                "code": "CSRF_INVALID_TOKEN",
                "details": "Invalid or missing CSRF token.",
            },
        },
    )


async def verify_csrf(
    request: Request,
    response: Response,
    csrf_protect: CsrfProtect = Depends(),
):
    """
    This is a FastAPI dependency function that verifies the CSRF token and unsets the cookie.

    example usage:
    ```python
    @router.post(
        "/login",
        ...
    )
    async def login(
        request: Request,
        response: Response,
        _: None = Depends(verify_csrf),
        ...
    )
    ```
    """
    try:
        await csrf_protect.validate_csrf(request)
        flow_logger.info("CSRF token validated successfully.")
    except CsrfProtectError:
        flow_logger.error("CSRF token validation failed.")
        raise
    csrf_protect.unset_csrf_cookie(response)
