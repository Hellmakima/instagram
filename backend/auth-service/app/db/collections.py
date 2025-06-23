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

def refresh_tokens_col(db: AsyncIOMotorDatabase):
    flow_logger.info("in refresh_tokens_col")
    return db.get_collection("refresh_tokens")