"""
File: app/core/security.py

Contains the security related functions like hashing, verifying passwords, creating access and refresh tokens etc.
JWT is used for authentication.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTClaimsError, JWTError
from passlib.context import CryptContext

from datetime import datetime, timedelta
from typing import Any, Union

from app.core.config import settings
from app.schemas.auth import TokenData
from app.core.config import settings

from app.db.db import get_db
from app.db.collections import users_col
from app.schemas.user import UserMe
from motor.motor_asyncio import AsyncIOMotorDatabase

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(
    data: TokenData,
    expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    # to_encode = {"exp": expire, "sub": {"username": data.username}, "type": "access"}
    to_encode = {"exp": expire, "sub": data.username, "type": "access"}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def create_refresh_token(
    data: TokenData,
    expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    # to_encode = {"exp": expire, "sub": {"username": data.username}, "type": "refresh"}
    to_encode = {"exp": expire, "sub": data.username, "type": "refresh"}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def verify_token(token: str, token_type: str = "access") -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        decoded_token = jwt.decode(
            token=token,
            key=settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        if decoded_token["type"] != token_type:
            raise credentials_exception
        return decoded_token["sub"]
    except HTTPException as e:
        # Re-raise any HTTPException
        raise e
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Token expired"
        )
    except JWTClaimsError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=f"Invalid claims: {e}"
        )
    except JWTError:
        raise credentials_exception

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncIOMotorDatabase = Depends(get_db)
) -> UserMe:
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
        # Re-raise any HTTPExceptions from verify_token
        raise e
    except JWTError:
        raise credentials_exception
    user = await users_col(db).find_one({"username": username})
    if user is None:
        raise credentials_exception
        
    return UserMe(**user)

