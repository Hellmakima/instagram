"""
### File: app/api/api_v1/router.py

Combines all the routers from api folder making it easier to import
"""

from fastapi import APIRouter

from app.api.api_v1.router import router as v1_router

router = APIRouter()

router.include_router(v1_router, prefix="/v1", tags=["v1"])
