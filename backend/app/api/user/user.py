"""
File: app/api/user/user.py

Contains the user related endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
# from bson import ObjectId

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.db import get_db
# from app.core.config import settings
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
)
# from app.schemas.user import UserCreate, User
from app.schemas.auth import AuthResponse, TokenData
from app.db.collections import users_col

router = APIRouter(prefix="/auth", tags=["auth"])
# router = APIRouter()

@router.post(
    "/register",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED
)
async def register(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    if await users_col(db).find_one({"username": form_data.username}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User exists"
        )

    user_doc = {
        "username": form_data.username,
        "hashed_password": get_password_hash(form_data.password),
    }
    res = await users_col(db).insert_one(user_doc)
    rec = await users_col(db).find_one({"_id": res.inserted_id})

    tok_data = TokenData(username=rec["username"])
    access_token = create_access_token(tok_data)
    refresh_token = create_refresh_token(tok_data)

    return AuthResponse(
        username=rec["username"],
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="Bearer",
    )

@router.post("/login", response_model=AuthResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    user = await users_col(db).find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid creds",
            headers={"WWW-Authenticate": "Bearer"},
        )

    tok_data = TokenData(username=user["username"])
    access_token = create_access_token(tok_data)
    refresh_token = create_refresh_token(tok_data)

    return AuthResponse(
        username=user["username"],
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="Bearer",
    )