# A'udhu billahi min ash-shaytan ir-rajim Bismillahi ar-Rahmani ar-Rahim

"""
### File: **app/main.py**

Contains the FastAPI app for the auth server
Collects all the routers from api folder and mounts them to the app
Manages the database connection

to run the app in /backend> uvicorn app.main:app --reload --port 5000
or hit f5 in vscode
"""

# mongodb connection client
from fastapi.staticfiles import StaticFiles
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

# fastapi app
from fastapi import FastAPI

# csrf protection
from app.core.csrf import csrf_exception_handler, CsrfProtectError
from app.api.api_v1.router import router

# startup
from contextlib import asynccontextmanager
import app.utils.loggers # initialize loggers

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    app.state.client = client
    
    await app.state.client.admin.command("ping")
    # TODO: Create indexes for all collections
    db = client.get_database()
    
    # this should be done only once.
    # await db.users.create_index("username", unique=True)
    
    yield
    client.close()

app = FastAPI(lifespan=lifespan, title="Auth Server", version="0.1")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.add_exception_handler(CsrfProtectError, csrf_exception_handler)
app.include_router(router)
