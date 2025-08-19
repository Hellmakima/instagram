# app/core/lifespan.py

from contextlib import asynccontextmanager
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    app.state.client = client
    await client.admin.command("ping")

    db = client.get_database()
    # Run this only once if needed
    await db.refresh_tokens.create_index(
        [("expires_at", 1)], expireAfterSeconds=0
    )
    await db.users.create_index(
        [("delete_at", 1)],
        expireAfterSeconds=0,
        partialFilterExpression={"is_deleted": True}
    )
    # already exists, doesn't make a difference
    await db.users.create_index("_id")


    yield
    client.close()
