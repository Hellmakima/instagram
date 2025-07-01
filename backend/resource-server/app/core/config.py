"""
### File: app/core/config.py

Contains the settings for the project
These are loaded from .env file.
"""
from dotenv import load_dotenv
from pydantic import Field, ValidationError, field_validator
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    MONGODB_URI: str = Field(..., description="MongoDB URI")
    MONGODB_DB: str = Field(..., description="MongoDB Database")
    CSRF_SECRET: str = Field(..., description="CSRF Secret")
    
    class Config:
        env_file = ".env"  # Load from .env file
        case_sensitive = True

try:
    settings = Settings()
except ValidationError as e:
    raise RuntimeError(f"Invalid configuration (.env file): {e}") from e
