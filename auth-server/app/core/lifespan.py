# app/core/lifespan.py

from contextlib import asynccontextmanager
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings

# TODO: collections names are hardcoded, maybe we can use a config file for this.
@asynccontextmanager
async def lifespan(app: FastAPI):
    client = AsyncIOMotorClient(
        settings.MONGODB_URI,
        # TODO: add these settings
        # username=settings.MONGODB_USERNAME,
        # password=settings.MONGODB_PASSWORD,
        # maxPoolSize=settings.MAX_DB_CONN_COUNT,
        # minPoolSize=settings.MIN_DB_CONN_COUNT,
        uuidRepresentation="standard",
    )
    app.state.client = client
    await client.admin.command("ping")

    db = client.get_database()
    # Run this only once if needed
    await db[settings.USER_COLLECTION].create_index(
        [("username", 1), ("email", 1)], unique=True
    )
    # await db[settings.REFRESH_TOKEN_COLLECTION].create_index(
    #     [("expires_at", 1)], expireAfterSeconds=0
    # )
    await db[settings.USER_COLLECTION].create_index(
        [("delete_at", 1)],
        expireAfterSeconds=0,
        partialFilterExpression={"is_pending_deletion": True}
    )
    # already exists, doesn't make a difference
    await db[settings.USER_COLLECTION].create_index("_id")

    yield
    client.close()
