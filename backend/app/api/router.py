"""
File: app/api/router.py

Combines all the routers from api folder making it easier to import
"""
# api/routes.py

from fastapi import APIRouter
from app.api.user import user

router = APIRouter()

router.include_router(user.router, prefix="/users", tags=["users"])
# router.include_router(posts.router, prefix="/posts", tags=["posts"])
# router.include_router(auth.router, prefix="/auth", tags=["auth"])
