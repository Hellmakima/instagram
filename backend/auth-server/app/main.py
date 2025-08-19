# A'udhu billahi min ash-shaytan ir-rajim Bismillahi ar-Rahmani ar-Rahim

"""
### File: **app/main.py**

Contains the FastAPI app for the auth server
Collects all the routers from api folder and mounts them to the app
Manages the database connection

to run the app in /backend> uvicorn app.main:app --reload --port 5000
or hit f5 in vscode
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.core.config import settings
from app.core.csrf import csrf_exception_handler, CsrfProtectError
from app.core.lifespan import lifespan
from app.api.api_v1.router import router

import app.utils.loggers  # initialize loggers

app = FastAPI(lifespan=lifespan, title="Auth Server", version="0.1")

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_exception_handler(CsrfProtectError, csrf_exception_handler)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(router)
