"""
### File: **app/main.py**

Contains the FastAPI app
Collects all the routers from api folder and mounts them to the app
Serves static files from static folder
Manages the database connection

to run the app in /backend> uvicorn app.main:app --reload --port 5000
or run backend/app/main.py
"""

# mongodb connection client
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from dotenv import load_dotenv
load_dotenv()

# fastapi app
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.router import router
from contextlib import asynccontextmanager
import app.utils.loggers

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

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router)

@app.get("/")
async def root(name: str="Sufiyan"):
    """
    Test endpoint
    call with http://localhost:5000/?name=Sufiyan
    or http://localhost:5000
    """
    return {"message": f"Hello from FastAPI",
            "name": name}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000, reload=True)