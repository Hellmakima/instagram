from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from app.db.repositories.user import User as UserRepository
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
    user = await user_repo.find_id_by_username(username)
    if user:
        return TokenData(id=user)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=APIErrorResponse(
                message="User not found",
                error=ErrorDetail(
                    code="USER_NOT_FOUND",
                    details="User not found."
                )
            ).model_dump()
        )