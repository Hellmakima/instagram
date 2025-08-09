"""
### File: app/core/db.py

Contains the database connection and related functions
"""

# app/core/db.py

from fastapi import Request
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.config import settings

async def get_db(request: Request) -> AsyncIOMotorDatabase:
    """
    Get MongoDB database from FastAPI app state.
    Usage: Depends(get_db)
    """
    return request.app.state.client[settings.MONGODB_DB]
