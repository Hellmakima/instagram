"""
### File: app/core/security.py

Contains the security related functions like hashing, verifying passwords, creating access and refresh tokens etc.
JWT is used for authentication.
"""
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTClaimsError, JWTError
from passlib.context import CryptContext

import asyncio
from datetime import datetime, timedelta, timezone

from app.core.config import settings
from app.schemas.auth import TokenData
from app.schemas.responses import APIErrorResponse, ErrorDetail
from app.core.config import settings

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
) -> str:
    flow_logger.info("in create_access_token")
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": data.id, "type": "access"}
    # to_encode (more data)= {"exp": expire, "sub": data.username, "type": "Bearer", "field": "value"}
    # encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    encoded_jwt = jwt.encode(to_encode, settings.ACCESS_TOKEN_PRIVATE_JWT_SECRET_KEY, algorithm=settings.ACCESS_TOKEN_JWT_ALGORITHM)
    return encoded_jwt


def create_refresh_token(
    data: TokenData,
) -> str:
    flow_logger.info("in create_refresh_token")
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": data.id, "type": "Bearer"}
    encoded_jwt = jwt.encode(to_encode, settings.REFRESH_TOKEN_JWT_SECRET_KEY, algorithm=settings.REFRESH_TOKEN_JWT_ALGORITHM)
    return encoded_jwt


def verify_token(
    token: str, 
    token_type: str,
) -> TokenData:
    """
    Verify the token and return the user's data.
    Raises HTTPException if the token is invalid or expired.
    """
    flow_logger.info("in verify_token")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=APIErrorResponse(
                    message="Credentials not valid",
                    error=ErrorDetail(
                        code="INVALID_CREDENTIALS",
                        details="The credentials provided are invalid or expired."
                    )
                ).model_dump(),
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        decoded_token = None
        if token_type == "access":
            decoded_token = jwt.decode(
                token=token,
                key=settings.ACCESS_TOKEN_PUBLIC_JWT_SECRET_KEY,
                algorithms=[settings.ACCESS_TOKEN_JWT_ALGORITHM]
            )
        elif token_type == "refresh":
            decoded_token = jwt.decode(
                token=token,
                key=settings.REFRESH_TOKEN_JWT_SECRET_KEY,
                algorithms=[settings.REFRESH_TOKEN_JWT_ALGORITHM]
            )
        else:
            flow_logger.error("Invalid token type: %s", token_type)
            raise credentials_exception
        if decoded_token["type"] != token_type:
            flow_logger.error("Invalid token type: %s", decoded_token["type"])
            raise credentials_exception
        return TokenData(id=decoded_token["sub"])
    except HTTPException as e:
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
            ).model_dump(),
            headers={"WWW-Authenticate": "Bearer"}
        )
    except JWTClaimsError as e:
        flow_logger.error("Invalid claims: %s", str(e))
        raise credentials_exception
    except JWTError:
        flow_logger.error("Error verifying token")
        raise credentials_exception
