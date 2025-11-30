# app/core/lifespan.py

from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.db import create_client, create_indexes
from app.core.config import settings
import redis.asyncio as redis
from fastapi_limiter import FastAPILimiter


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Mongo client
    client = await create_client()
    app.state.client = client

    await create_indexes(client.get_database())

    # Redis connection (for fastapi-limiter)
    redis_conn = redis.from_url(
        settings.REDIS_URL, encoding="utf-8", decode_responses=True
    )
    await FastAPILimiter.init(redis_conn)

    yield

    client.close()
