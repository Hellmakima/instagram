"""
### File: **app/api/router.py**

Combines all the routers from api folder making it easier to import
"""
# api/routes.py

from fastapi import APIRouter
from app.api.api_v1.user.user import router as user_router
from app.api.api_v1.auth.auth import router as auth_router

router = APIRouter()

router.include_router(auth_router, tags=["auth"], prefix="/auth")
router.include_router(user_router, tags=["user"], prefix="/user")
