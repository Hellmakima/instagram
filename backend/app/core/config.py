"""
File: app/core/config.py

Contains the settings for the project
"""
from dotenv import load_dotenv
from pydantic import BaseSettings, Field, ValidationError

load_dotenv()

class Settings(BaseSettings):
    MONGODB_URI: str = Field(..., description="MongoDB URI")
    MONGODB_DB: str = Field(..., description="MongoDB Database")
    CSRF_SECRET: str = Field(..., description="CSRF Secret")
    JWT_SECRET_KEY: str = Field(..., description="JWT Secret Key")
    if not JWT_SECRET_KEY:
        raise ValueError("JWT_SECRET_KEY environment variable missing")
    JWT_ALGORITHM: str = Field("HS256", description="JWT Algorithm")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, description="Access Token Expire Minutes")
    
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(30, description="Refresh Token Expire Days")
    REFRESH_TOKEN_EXPIRE_MINUTES: int = Field(REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60, description="Refresh Token Expire Minutes")
    class Config:
        env_file = ".env"  # Load from .env file
        case_sensitive = True

try:
    settings = Settings()
except ValidationError as e:
    raise RuntimeError(f"Invalid configuration (.env file): {e}") from e
