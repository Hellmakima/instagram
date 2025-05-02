"""
File: app/api/auth/auth.py

Contains the authentication related endpoints
"""
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
# from fastapi import Request
from fastapi.security import OAuth2PasswordRequestForm
# from bson import ObjectId

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.db import get_db
from app.core.config import settings
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
)
# from app.schemas.user import UserCreate, User
from app.schemas.auth import AuthResponse, TokenData
from app.db.collections import users_col, refresh_tokens_col

import logging
from logging.config import dictConfig

LOG_CONFIG = {
    "version": 1,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

dictConfig(LOG_CONFIG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

router = APIRouter(prefix="/auth", tags=["auth"])
# router = APIRouter()

def validate_password(password: str):
    if len(password) < 8:
        raise HTTPException(400, "Password must be ≥8 characters")
    # Add checks for uppercase, numbers, etc.

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
    validate_password(form_data.password)
    user_doc = {
        "username": form_data.username,
        "hashed_password": get_password_hash(form_data.password),
    }
    res = await users_col(db).insert_one(user_doc)
    rec = await users_col(db).find_one({"_id": res.inserted_id})

    tok_data = TokenData(username=rec["username"])
    access_token = create_access_token(tok_data)
    refresh_token = create_refresh_token(tok_data)

    logger.info("User %s registered", rec["username"])
    
    return AuthResponse(
        username=rec["username"],
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="Bearer",
    )

@router.post("/login", response_model=AuthResponse)
async def login(
    # request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    user = await users_col(db).find_one(
        {"username": form_data.username}, 
        projection={"hashed_password": 1, "username": 1}
    )
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        logger.error(
            "Failed login attempt for username: %s (IP: %s)",
            form_data.username,
            # request.client.host
            # TODO: implement this to add IP address of client. gets complicated if using reverse proxy
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid creds",
            headers={"WWW-Authenticate": "Bearer"},
        )

    tok_data = TokenData(username=user["username"])
    access_token = create_access_token(tok_data)
    refresh_token = create_refresh_token(tok_data)
    
    await refresh_tokens_col(db).insert_one({
        "user_id": user["_id"],
        "refresh_token": refresh_token,
        "expires_at": datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES),
        "revoked": False
    })
    
    logger.info("User %s logged in", user["username"])
    
    return AuthResponse(
        username=user["username"],
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="Bearer",
    )