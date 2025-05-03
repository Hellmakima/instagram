"""
File: app/api/user/user.py

Contains the user related endpoints
"""

from fastapi import APIRouter, Depends
from app.schemas.user import UserMe
from app.core.security import get_current_user

router = APIRouter(prefix="/user", tags=["user"])
# router = APIRouter()

@router.get(
    "/me",
    response_model=UserMe,
    summary="Get current user details",
    description="Returns authenticated user's profile information"
)
async def read_current_user(
    current_user: UserMe = Depends(get_current_user)
):
    print('in me')
    """
    Temp function for testing
    Get details for the currently authenticated user
    """
    return current_user