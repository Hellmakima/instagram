"""
File: app/api/user/user.py

Contains the user related endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

from app.core.db import get_db
from app.core.config import settings
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
)
from app.schemas.user import UserCreate, User
from app.schemas.auth import AuthResponse

router = APIRouter(prefix="/auth", tags=["auth"])
def users_col(db: AsyncIOMotorDatabase):
    return db[settings.MONGODB_NAME]["users"]


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    if await users_col(db).find_one({"username": user.username}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            details="User exists"
        )
    data = user.dict()
    data["hashed_password"] = get_password_hash(user.password)
    res = await users_col(db).insert_one(data)
    rec = await users_col(db).find_one({"_id": res.inserted_id})
    
    token_data = TokenData(username=rec["username"])
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return AuthResponse(
        user=user.username,
        access_token=access_token,
        refresh_token=refresh_token,
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
            detail="Invalid credentials"
        )
    token_data = TokenData(username=user["username"])
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    return AuthResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )
