"""
### File: app/core/security.py

Contains the security related functions like hashing, verifying passwords, creating access and refresh tokens etc.
JWT is used for authentication.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTClaimsError, JWTError
from passlib.context import CryptContext

import asyncio
from datetime import datetime, timedelta, timezone

from app.core.config import settings
from app.schemas.auth import APIErrorResponse, ErrorDetail, TokenData
from app.core.config import settings

from app.db.db import get_db
from app.db.collections import users_col
from app.schemas.user import UserMe
from motor.motor_asyncio import AsyncIOMotorDatabase

import logging
flow_logger = logging.getLogger("app_flow")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_password_hash(password: str) -> str:
    flow_logger.info("in get_password_hash")
    return await asyncio.to_thread(pwd_context.hash, password)


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    flow_logger.info("in verify_password")
    return await asyncio.to_thread(pwd_context.verify, plain_password, hashed_password)


def create_access_token(
    data: TokenData,
    expires_delta: timedelta = None
) -> str:
    flow_logger.info("in create_access_token")
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": data.id, "type": "Bearer"}
    # to_encode (more data)= {"exp": expire, "sub": data.username, "type": "Bearer", "field": "value"}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def create_refresh_token(
    data: TokenData,
    expires_delta: timedelta = None
) -> str:
    flow_logger.info("in create_refresh_token")
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": data.id, "type": "Bearer"}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def verify_token(token: str, token_type: str = "Bearer") -> TokenData:
    flow_logger.info("in verify_token")
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
            flow_logger.error("Invalid token type: %s", decoded_token["type"])
            raise credentials_exception
        return TokenData(decoded_token["sub"])
    except HTTPException as e:
        flow_logger.error("Error verifying token: %s", str(e))
        raise
    except ExpiredSignatureError:
        flow_logger.error("Token expired")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=APIErrorResponse(
                message="Token expired",
                error=ErrorDetail(
                    code="TOKEN_EXPIRED",
                    details="Token expired"
                )
            ).model_dump()
        )
    except JWTClaimsError as e:
        flow_logger.error("Invalid claims: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=APIErrorResponse(
                message="Invalid claims",
                error=ErrorDetail(
                    code="INVALID_CLAIMS",
                    details=f"Invalid claims: {e}"
                )
            ).model_dump()
        )
    except JWTError:
        flow_logger.error("Error verifying token")
        raise credentials_exception

# async def get_current_user(
'''
# TODO: rework on this
- no need to verify token here
- look up what is `token: str = Depends(oauth2_scheme)`
'''
#     token: str = Depends(oauth2_scheme),
#     db: AsyncIOMotorDatabase = Depends(get_db)
# ) -> UserMe:
#     # TODO: Decide if I really get_current_user() or repurpose it.
#     flow_logger.info("in get_current_user")
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
    
#     try:
#         user = verify_token(token)
#         if not user:
#             raise credentials_exception
#     except HTTPException as e:
#         flow_logger.error("Error verifying token: %s", str(e))
#         # Re-raise any HTTPExceptions from verify_token
#         raise e
#     except JWTError:
#         flow_logger.error("Error verifying token")
#         raise credentials_exception
#     user_data = await users_col(db).find_one(
#         {"_id": user.id},
#         projection={"_id": 1, "username": 1}
#     )
#     if not user_data:
#         flow_logger.error("User not found in DB")
#         raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail="User not found",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     return UserMe(**user_data)

