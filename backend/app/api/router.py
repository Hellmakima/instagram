"""
File: app/api/router.py

Combines all the routers from api folder making it easier to import
"""
# api/routes.py

from fastapi import APIRouter
from app.api.user import user
from app.api.auth import auth

router = APIRouter()

router.include_router(auth.router, tags=["auth"])
router.include_router(user.router, tags=["user"])
