# app/api/dependencies/db_deps.py

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorClient
from app.db.db import get_db, get_client
from app.db.repositories.user_repo import UserRepository


def get_user_repo(db: AsyncIOMotorDatabase = Depends(get_db)) -> UserRepository:
    """Provides a UserRepository instance with a database connection."""
    # Gemini says: Every time your code asks for get_user_repo within the context of that one request, FastAPI doesn't re-run the function. It just provides the same UserRepository object that was created the first time. The same applies to the database connection object from get_db.
    return UserRepository(db)

async def get_session(client: AsyncIOMotorClient = Depends(get_client)):
    async with await client.start_session() as session:
        yield session