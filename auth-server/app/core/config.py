"""
### File: app/core/config.py

Contains the settings for the project
These are loaded from .env file.
"""
from dotenv import load_dotenv
from pydantic import Field, ValidationError, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    # MongoDB
    MONGODB_URI: str = Field(..., description="MongoDB URI")
    MONGODB_DBNAME: str = Field(..., description="MongoDB Database")
    USER_COLLECTION: str = Field(..., description="User collection name")
    REFRESH_TOKEN_COLLECTION: str = Field(..., description="Refresh token collection name")

    # CSRF
    CSRF_SECRET: str = Field(..., description="CSRF Secret")

    # Refresh Token (HS256)
    REFRESH_TOKEN_JWT_SECRET_KEY: str = Field(..., description="Secret key for refresh tokens")
    REFRESH_TOKEN_JWT_ALGORITHM: str = Field(..., description="Algorithm for refresh tokens")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(..., description="Refresh token expire days")
    REFRESH_TOKEN_EXPIRE_MINUTES: int = Field(1, description="Refresh token expire minutes")

    # Access Token (RS256)
    ACCESS_TOKEN_PUBLIC_JWT_SECRET_KEY: str = Field(..., description="Public key for access tokens")
    ACCESS_TOKEN_PRIVATE_JWT_SECRET_KEY: str = Field(..., description="Private key for access tokens")
    ACCESS_TOKEN_JWT_ALGORITHM: str = Field(..., description="Algorithm for access tokens")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(..., description="Access token expire minutes")

    @field_validator('REFRESH_TOKEN_EXPIRE_MINUTES', mode='before')
    @classmethod
    def set_refresh_minutes(cls, v, info):
        days = info.data.get('REFRESH_TOKEN_EXPIRE_DAYS', 30)
        return days * 24 * 60

try:
    settings = Settings()  # type: ignore
except ValidationError as e:
    raise RuntimeError(f"Invalid configuration (.env file): {e}") from e
