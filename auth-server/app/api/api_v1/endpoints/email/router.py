# app/api/api_v1/endpoints/email/router.py

from app.services.email.verification import send_verification_email as send_verification_email_service
from app.services.email.verification import verify_email_token as verify_email_token_service
from app.repositories.interfaces import UserRepositoryInterface as UserRepository
from app.api.dependencies.db_deps import get_user_repo
from fastapi import APIRouter, Depends, Request, status
from app.core.csrf import verify_csrf
from app.schemas.responses import (
    APIErrorResponse,
    SuccessMessageResponse,
)
from app.schemas.auth import UserId as UserIdSchema

router = APIRouter()

"""
TODO:
This is trash and needs to be rewritten properly.
There is no proper use of schemas, responses, error handling, logging, etc.
Use `from fastapi import Query` for query params.
"""

@router.get(
    "/send-verification-email",
    response_model=SuccessMessageResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": APIErrorResponse, "description": "Bad Request"},
        403: {"model": APIErrorResponse, "description": "Forbidden (CSRF error)"},
        500: {"model": APIErrorResponse, "description": "Internal Server Error"},
    }
)
async def send_verification_email(
    form_data: UserIdSchema,
    request: Request,
    _: None = Depends(verify_csrf),
    user_repo: UserRepository = Depends(get_user_repo),
):
    """
    Generates a verification token and sends the verification email to the user.
    """
    # Expect query params: user_id and email (email optional if user exists)
    params = dict(request.query_params)
    user_id = params.get("user_id")
    email = params.get("email")

    # If user_id provided, fetch user to get email if not provided
    if user_id and not email:
        user = await user_repo.get_by_id(user_id)
        if not user:
            return {"ok": False, "detail": "user not found"}
        email = getattr(user, "email", None)

    if not email or not user_id:
        return {"ok": False, "detail": "missing user_id or email"}

    # build token data and call service
    from app.schemas.auth import TokenData

    token_data = TokenData(id=user_id)
    sent = await send_verification_email_service(token_data, email)
    return {"ok": bool(sent)}


@router.get("/verify-email")
async def verify_email(
    token: str,
    user_repo: UserRepository = Depends(get_user_repo),
):
    """
    Verify an email verification token and mark user as verified.
    """
    user_id = await verify_email_token_service(token, user_repo)
    if user_id:
        return {"ok": True, "user_id": user_id}
    return {"ok": False}