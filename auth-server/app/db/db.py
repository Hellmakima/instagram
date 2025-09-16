"""
### File: app/db/db.py

Contains the database connection and client.
"""

from fastapi import Request
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorClient
# from pymongo.errors import ConnectionFailure
# import asyncio

from app.core.config import settings
# from config import settings

async def get_db(request: Request) -> AsyncIOMotorDatabase:
    # TODO: see why this needs request.
    """
    Get MongoDB database from FastAPI app state.
    Usage: Depends(get_db)
    """
    return request.app.state.client[settings.MONGODB_DBNAME]

async def get_client(request: Request) -> AsyncIOMotorClient:
    return request.app.state.client
