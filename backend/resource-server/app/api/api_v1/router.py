"""
### File: **app/api/router.py**

Combines all the routers from api folder making it easier to import
"""
# api/routes.py

from fastapi import APIRouter
from app.api.api_v1.user.user import router as user_router

router = APIRouter()

router.include_router(user_router, tags=["user"], prefix="/user")
