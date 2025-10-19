# app/services/user/get_user.py

from app.repositories.interfaces import UserRepositoryInterface as UserRepository

async def get_user(user_id: str, user_repo: UserRepository):
    """
    Get user by user_id.
    """
    return await user_repo.get_by_id(user_id)

async def get_user_by_username(username: str, user_repo: UserRepository):
    """
    Get user by username.
    """
    return await user_repo.get_by_username_or_email(username)