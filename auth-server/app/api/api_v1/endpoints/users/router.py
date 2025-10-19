from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from app.repositories.interfaces import UserRepositoryInterface as UserRepository
from app.api.dependencies.db_deps import get_user_repo
from app.schemas.auth import TokenData
from app.schemas.responses import (
    APIErrorResponse, 
    ErrorDetail, 
)

router = APIRouter()

@router.get("/{username}", response_model=TokenData)
async def get_user_by_username(
    username: str,
    user_repo: UserRepository = Depends(get_user_repo)
):
    """
    Get user_id by username.
    """
    return await user_repo.get_by_username(username)
