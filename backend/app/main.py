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
from app.api.api_v1.router import router
from fastapi.middleware.cors import CORSMiddleware

# startup
from contextlib import asynccontextmanager

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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router)

from fastapi.responses import HTMLResponse
@app.get("/", response_class=HTMLResponse)
async def root(name: str = "Sufiyan"):
    return f"""
    <html>
        <body>
            <h2>Hello {name}</h2>
            <ul>
                <li><a href="/static/login.html">Login Page</a></li>
                <li><a href="/static/index.html">Index Page</a></li>
                <li><a href="/static/test/login.html">Test Login</a></li>
                <li><a href="/static/test/me.html">Test Me</a></li>
                <li><a href="/docs">Swagger Docs</a></li>
            </ul>
        </body>
    </html>
    """
