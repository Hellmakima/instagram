"""
### File: app/db/collections.py

Contains the database collections
"""
from motor.motor_asyncio import AsyncIOMotorDatabase
import logging

flow_logger = logging.getLogger("app_flow")

def users_col(db: AsyncIOMotorDatabase):
    flow_logger.info("in users_col")
    return db.get_collection("users")