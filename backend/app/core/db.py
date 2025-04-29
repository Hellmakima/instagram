"""
File: app/core/db.py

Contains the database connection and related functions
"""

# app/core/db.py

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import ConnectionFailure
import asyncio

try:
    from app.core.config import settings
except ImportError:
    from config import settings

try:
    from main import client  # when used inside project
except ImportError:
    client: AsyncIOMotorClient = AsyncIOMotorClient(settings.MONGODB_URI)  # when running directly
    
async def get_db() -> AsyncIOMotorDatabase:
    await client.admin.command("ping")
    return client[settings.MONGODB_DB]

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
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(test_db_connection())