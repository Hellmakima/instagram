"""
### File: app/api/user/user.py

Contains the user related endpoints
"""

from fastapi import APIRouter, Depends
from app.schemas.user import UserMe
from app.core.security import get_current_user
import logging

router = APIRouter()
flow_logger = logging.getLogger("app_flow")

@router.get(
    "/me",
    response_model=UserMe,
    summary="Get current user details",
    description="Returns authenticated user's profile information"
)
async def read_current_user(
    current_user: UserMe = Depends(get_current_user)
):
    """
    Temp function for testing
    Get details for the currently authenticated user
    """
    flow_logger.info("in read_current_user")
    return current_user