"""
### File: app/core/db.py

Contains the database connection and related functions
"""

# app/core/db.py

from fastapi import Request
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import ConnectionFailure
import asyncio

from app.core.config import settings
# from config import settings

async def get_db(request: Request) -> AsyncIOMotorDatabase:
    """
    Get MongoDB database from FastAPI app state.
    Usage: Depends(get_db)
    """
    return request.app.state.client[settings.MONGODB_DB]

async def test_db_connection():
    """
    Async test: insert, query, delete.
    """
    try:
        db = await get_db()
        coll = db.test_collection

        # 1. Insert
        test_doc = {"name": "Test User", "value": 123}
        res = await coll.insert_one(test_doc)
        print(f"Inserted ID: {res.inserted_id}")

        # 2. Query
        found = await coll.find_one({"_id": res.inserted_id})
        print(f"Found: {found}")

        assert found["name"] == "Test User"
        print("Data integrity OK")

        # 3. Cleanup
        await coll.delete_one({"_id": res.inserted_id})
        print("Cleaned up test doc")

    except ConnectionFailure as e:
        print(f"Mongo ping failed: {e}")
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_db_connection())