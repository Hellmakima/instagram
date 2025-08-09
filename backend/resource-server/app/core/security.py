"""
### File: app/core/security.py

Contains the security related functions like hashing, verifying passwords, creating access and refresh tokens etc.
JWT is used for authentication.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from jose.exceptions import JWTError
from passlib.context import CryptContext

from app.core.config import settings

from app.db.db import get_db
from app.db.collections import users_col
from app.schemas.user import UserMe
from motor.motor_asyncio import AsyncIOMotorDatabase

import logging
flow_logger = logging.getLogger("app_flow")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncIOMotorDatabase = Depends(get_db)
) -> UserMe:
    flow_logger.info("in get_current_user")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        username = verify_token(token)
        if not username:
            raise credentials_exception
    except HTTPException as e:
        flow_logger.error("Error verifying token: %s", str(e))
        # Re-raise any HTTPExceptions from verify_token
        raise e
    except JWTError:
        flow_logger.error("Error verifying token")
        raise credentials_exception
    user = await users_col(db).find_one({"username": username})
    if user is None:
        raise credentials_exception
        
    return UserMe(**user)

