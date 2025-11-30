# tests/unit/schemas/test_auth.py
import pytest
from pydantic import ValidationError
from app.schemas import auth


def test_username_validator_valid():
    valid = ["user_01", "abc.DEF-123", "name"]
    for u in valid:
        obj = auth.UserCreate(
            username=u, email="test@gmail.com", password="Aa1!password"
        )
        assert obj.username == u


def test_username_validator_invalid():
    invalid = ["user$", "name!", "space name"]
    for u in invalid:
        with pytest.raises(ValidationError):
            auth.UserCreate(username=u, email="test@gmail.com", password="Aa1!password")


def test_email_validator_valid():
    obj = auth.UserCreate(
        username="user1", email="test@gmail.com", password="Aa1!password"
    )
    assert obj.email == "test@gmail.com"


def test_email_validator_invalid():
    with pytest.raises(ValidationError):
        auth.UserCreate(
            username="user1", email="test@yahoo.com", password="Aa1!password"
        )


def test_password_validator_valid():
    obj = auth.UserCreate(
        username="user1", email="test@gmail.com", password="Abcdef1!23"
    )
    assert obj.password == "Abcdef1!23"


def test_password_validator_invalid_missing_uppercase():
    with pytest.raises(ValidationError):
        auth.UserCreate(username="user1", email="test@gmail.com", password="abcdef1!")


def test_password_validator_invalid_missing_lowercase():
    with pytest.raises(ValidationError):
        auth.UserCreate(username="user1", email="test@gmail.com", password="ABCDEF1!")


def test_password_validator_invalid_missing_digit():
    with pytest.raises(ValidationError):
        auth.UserCreate(username="user1", email="test@gmail.com", password="Abcdefgh!")


def test_password_validator_invalid_missing_special():
    with pytest.raises(ValidationError):
        auth.UserCreate(username="user1", email="test@gmail.com", password="Abcdefg1")


def test_password_contains_username_or_email():
    with pytest.raises(ValidationError):
        auth.UserCreate(username="user1", email="test@gmail.com", password="user1Aa1!")
    with pytest.raises(ValidationError):
        auth.UserCreate(username="user1", email="test@gmail.com", password="testAa1!")
