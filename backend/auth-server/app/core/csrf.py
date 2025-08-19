# app/core/csrf.py

from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError
from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic_settings import BaseSettings
import dotenv
from app.schemas.responses import InternalServerError

import logging
security_logger = logging.getLogger("security_logger")

# TODO: rewrite this
class CsrfSettings(BaseSettings):
    secret_key: str|None = dotenv.dotenv_values(".env")["CSRF_SECRET"]
    if secret_key is None:
        security_logger.error("CSRF secret key not found in .env file.")
        raise InternalServerError()
    cookie_samesite: str = "lax"
    cookie_secure: bool = False # HTTPS only
    header_name: str = "X-CSRF-Token"

@CsrfProtect.load_config
def get_csrf_config():
    return CsrfSettings()


def csrf_exception_handler(request: Request, exc: Exception):
    if not isinstance(exc, CsrfProtectError):
        raise exc  # re-raise if not the expected exception

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": "CSRF validation failed",
            "error": {
                "code": "CSRF_INVALID_TOKEN",
                "details": "Invalid or missing CSRF token."
            }
        }
    )
