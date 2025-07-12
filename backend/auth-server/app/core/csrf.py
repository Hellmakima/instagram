# app/core/csrf.py
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError
from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic_settings import BaseSettings

class CsrfSettings(BaseSettings):
    secret_key: str = "asecrettoeverybody"          # TODO: pull from .env
    cookie_samesite: str = "none"
    cookie_secure: bool = True                      # HTTPS only!

@CsrfProtect.load_config
def get_csrf_config():
    return CsrfSettings()

def csrf_exception_handler(request: Request, exc: CsrfProtectError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})
