
import pytest
from app.db.db import get_db
from app.db.collections import users_col
from app.schemas.user import UserMe
from motor.motor_asyncio import AsyncIOMotorDatabase
import asyncio

@pytest.mark.asyncio
async def test_db_connection():
    # TODO: test db connection and perform test operations
    pass