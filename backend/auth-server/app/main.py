# A'udhu billahi min ash-shaytan ir-rajim Bismillahi ar-Rahmani ar-Rahim

"""
### File: **app/main.py**

Contains the FastAPI app for the auth server
Collects all the routers from api folder and mounts them to the app
Manages the database connection

to run the app in /backend> uvicorn app.main:app --reload --port 5000
or hit f5 in vscode
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.core.config import settings
from app.core.csrf import csrf_exception_handler, CsrfProtectError
from app.api.api_v1.router import router

import app.utils.loggers  # initialize loggers

@asynccontextmanager
async def lifespan(app: FastAPI):
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    app.state.client = client
    await client.admin.command("ping")
    # TODO: create indexes once here, e.g.
    # db = client.get_database()
    # await db.users.create_index("username", unique=True)
    yield
    client.close()

app = FastAPI(lifespan=lifespan, title="Auth Server", version="0.1")

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_exception_handler(CsrfProtectError, csrf_exception_handler)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(router)
