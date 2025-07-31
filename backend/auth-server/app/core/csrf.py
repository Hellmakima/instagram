# app/core/csrf.py
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError
from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic_settings import BaseSettings
import dotenv

class CsrfSettings(BaseSettings):
    secret_key: str = dotenv.dotenv_values(".env")["CSRF_SECRET"]
    cookie_samesite: str = "none"
    cookie_secure: bool = True                      # HTTPS only
    header_name: str = "X-CSRFToken"

@CsrfProtect.load_config
def get_csrf_config():
    return CsrfSettings()

def csrf_exception_handler(request: Request, exc: CsrfProtectError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})
