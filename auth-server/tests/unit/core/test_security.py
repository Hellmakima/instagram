import pytest
from fastapi import HTTPException
from jose import jwt

from app.core import security
from app.schemas.auth import TokenData
from app.core.config import settings


@pytest.fixture
def user_data():
    return TokenData(id="test_user")


@pytest.fixture
def access_token(user_data):
    return security.create_access_token(user_data)


@pytest.fixture
def refresh_token(user_data):
    return security.create_refresh_token(user_data)


@pytest.mark.asyncio
async def test_password_hash_and_verify():
    password = "s3cret!"

    hashed = await security.get_password_hash(password)
    assert hashed != password
    assert await security.verify_password(password, hashed)
    assert not await security.verify_password("wrong", hashed)


def test_create_access_token(user_data):
    token = security.create_access_token(user_data)
    decoded = jwt.decode(
        token,
        settings.ACCESS_TOKEN_PUBLIC_JWT_SECRET_KEY,
        algorithms=[settings.ACCESS_TOKEN_JWT_ALGORITHM],
    )
    assert decoded["sub"] == user_data.id
    assert decoded["type"] == "access"
    assert "exp" in decoded


def test_create_refresh_token(user_data):
    token = security.create_refresh_token(user_data)
    decoded = jwt.decode(
        token,
        settings.REFRESH_TOKEN_JWT_SECRET_KEY,
        algorithms=[settings.REFRESH_TOKEN_JWT_ALGORITHM],
    )
    assert decoded["sub"] == user_data.id
    assert decoded["type"] == "refresh"
    assert "exp" in decoded


def test_verify_access_token(access_token, user_data):
    result = security.verify_token(access_token, "access")
    assert result.id == user_data.id


def test_verify_refresh_token(refresh_token, user_data):
    result = security.verify_token(refresh_token, "refresh")
    assert result.id == user_data.id


def test_verify_token_type_mismatch(access_token):
    with pytest.raises(HTTPException) as exc:
        security.verify_token(access_token, "refresh")
    assert exc.value.status_code == 401
    assert "INVALID_CREDENTIALS" in str(exc.value.detail)


def test_verify_token_invalid_type_arg():
    with pytest.raises(HTTPException):
        security.verify_token("fake", "nonsense")


def test_verify_token_expired(monkeypatch):
    # here monkeypatch is necessary to simulate expired token
    def raise_expired(*args, **kwargs):
        raise security.ExpiredSignatureError()

    monkeypatch.setattr(security.jwt, "decode", raise_expired)
    with pytest.raises(HTTPException) as exc:
        security.verify_token("fake", "access")

    assert exc.value.status_code == 401
    assert "TOKEN_EXPIRED" in str(exc.value.detail)
