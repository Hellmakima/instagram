# app/core/lifespan.py

from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.db import create_client, create_indexes
from app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    client = await create_client()
    app.state.client = client

    await create_indexes(client.get_database())

    yield
    client.close()
