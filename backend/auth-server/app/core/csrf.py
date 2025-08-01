# app/core/csrf.py

from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError
from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic_settings import BaseSettings
import dotenv
from app.schemas.auth import ErrorDetail, APIErrorResponse

# TODO: rewrite this
class CsrfSettings(BaseSettings):
    secret_key: str = dotenv.dotenv_values(".env")["CSRF_SECRET"]
    cookie_samesite: str = "lax"
    cookie_secure: bool = False                      # HTTPS only
    header_name: str = "X-CSRF-Token"

@CsrfProtect.load_config
def get_csrf_config():
    return CsrfSettings()

def csrf_exception_handler(request: Request, exc: CsrfProtectError):
    return JSONResponse(
        status_code=exc.status_code, 
        content=APIErrorResponse(
            message="CSRF validation failed",
            error=ErrorDetail(
                code="CSRF_INVALID_TOKEN",
                details="Invalid or missing CSRF token."
            )
        ).model_dump()
    )
