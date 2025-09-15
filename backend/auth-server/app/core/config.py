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

    MONGODB_URI: str = Field(..., description="MongoDB URI")
    MONGODB_DBNAME: str = Field(..., description="MongoDB Database")
    USER_COLLECTION: str = Field(..., description="User Database")
    REFRESH_TOKEN_COLLECTION: str = Field(..., description="Refresh Token Database")
    CSRF_SECRET: str = Field(..., description="CSRF Secret")
    
    JWT_SECRET_KEY: str = Field(..., description="JWT Secret Key")
    JWT_ALGORITHM: str = Field(..., description="JWT Algorithm")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(..., description="Access Token Expire Minutes")

    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(..., description="Refresh Token Expire Days")
    REFRESH_TOKEN_EXPIRE_MINUTES: int = Field(1, description="Refresh Token Expire Minutes")

    @field_validator('REFRESH_TOKEN_EXPIRE_MINUTES', mode='before')
    @classmethod
    def set_refresh_minutes(cls, v, info):
        days = info.data.get('REFRESH_TOKEN_EXPIRE_DAYS', 30)
        return days * 24 * 60

try:
    settings = Settings() # type: ignore
except ValidationError as e:
    raise RuntimeError(f"Invalid configuration (.env file): {e}") from e
