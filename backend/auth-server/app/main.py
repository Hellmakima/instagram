# A'udhu billahi min ash-shaytan ir-rajim Bismillahi ar-Rahmani ar-Rahim

"""
### File: **app/main.py**

Contains the FastAPI app
Collects all the routers from api folder and mounts them to the app
Serves static files from static folder
Manages the database connection

to run the app in /backend> uvicorn app.main:app --reload --port 5000
or hit f5 in vscode
"""

# mongodb connection client
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from dotenv import load_dotenv
load_dotenv()

# fastapi app
from fastapi import FastAPI
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
    # Create indexes 
    # TODO: Create indexes for all collections
    db = client.get_database()
    await db.users.create_index("username", unique=True)
    
    yield
    client.close()

app = FastAPI(lifespan=lifespan, title="Auth Server", version="0.1")

app.include_router(router)

from fastapi.responses import HTMLResponse
@app.get("/", response_class=HTMLResponse)
async def root(name: str = "Sufiyan"):
    return f"""
    <html>
        <body>
            <h2>Auth working</h2>
        </body>
    </html>
    """
