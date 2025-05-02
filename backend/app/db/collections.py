"""
File: app/db/collections.py

Contains the database collections
"""
from motor.motor_asyncio import AsyncIOMotorDatabase

def users_col(db: AsyncIOMotorDatabase):
    return db.get_collection("users")

def refresh_tokens_col(db: AsyncIOMotorDatabase):
    return db.get_collection("refresh_tokens")