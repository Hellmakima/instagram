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

async def create_client():
    """Create a MongoDB client."""
    client = AsyncIOMotorClient(
        settings.MONGODB_URI,
        # TODO: add these settings
        # username=settings.MONGODB_USERNAME,
        # password=settings.MONGODB_PASSWORD,
        # maxPoolSize=settings.MAX_DB_CONN_COUNT,
        # minPoolSize=settings.MIN_DB_CONN_COUNT,
        uuidRepresentation="standard",
    )
    await client.admin.command("ping")
    return client

async def get_db(request: Request) -> AsyncIOMotorDatabase:
    # TODO: see why this needs request.
    """
    Get MongoDB database from FastAPI app state.
    Usage: Depends(get_db)
    """
    return request.app.state.client[settings.MONGODB_DBNAME]

async def get_client(request: Request) -> AsyncIOMotorClient:
    return request.app.state.client

async def create_indexes(db: AsyncIOMotorDatabase):
    """Create necessary indexes for the database collections."""

    # Run this only once if needed
    # if already exists, doesn't make a difference
    await db[settings.USER_COLLECTION].create_index(
        [("username", 1), ("email", 1)], unique=True
    )
    await db[settings.USER_COLLECTION].create_index(
        [("delete_at", 1)],
        expireAfterSeconds=0,
        partialFilterExpression={"is_pending_deletion": True}
    )
    # _id index already exists in mongo
    # await db[settings.USER_COLLECTION].create_index("_id")


    # Refresh tokens collection
    await db[settings.REFRESH_TOKEN_COLLECTION].create_index(
        [("refresh_token", 1)], unique=True
    )
    # Expire tokens only after they actually expire, keeping revoked tokens for audit
    await db[settings.REFRESH_TOKEN_COLLECTION].create_index(
        [("expires_at", 1)], expireAfterSeconds=3600*24*30  # 30 days after expiry
    )
    # Partial index to quickly find revoked tokens
    await db[settings.REFRESH_TOKEN_COLLECTION].create_index(
        [("revoked", 1), ("user_id", 1)],
        partialFilterExpression={"revoked": True}
    )
    # Compound index for querying active tokens per user efficiently
    await db[settings.REFRESH_TOKEN_COLLECTION].create_index(
        [("user_id", 1), ("revoked", 1), ("expires_at", 1)]
    )

