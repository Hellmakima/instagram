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
from app.schemas.user import UserCreate, User, Token

router = APIRouter(prefix="/auth", tags=["auth"])
def users_col(db: AsyncIOMotorDatabase):
    return db[settings.MONGODB_NAME]["users"]

from app.schemas.user import UserCreate, User, Token, AuthResponse  # define AuthResponse

class AuthResponse(BaseModel):
    user: User
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    if await users_col(db).find_one({"username": user_in.username}):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "User exists")
    data = user_in.dict()
    data["hashed_password"] = get_password_hash(user_in.password)
    res = await users_col(db).insert_one(data)
    rec = await users_col(db).find_one({"_id": res.inserted_id})
    rec["id"] = str(rec["_id"])

    uid = rec["id"]
    access_token = create_access_token(subject=uid)
    refresh_token = create_refresh_token(subject=uid)

    return AuthResponse(
        user=User(**rec),
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    user = await users_col(db).find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    uid = str(user["_id"])
    access_token = create_access_token(subject=uid)
    refresh_token = create_refresh_token(subject=uid)
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )
