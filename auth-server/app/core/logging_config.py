"""
### File: **app/core/logging_config.py**

Contains the settings for logging of the project
These are not loaded from .env file.
"""

from pydantic import ValidationError
from pydantic_settings import BaseSettings

class LogSettings(BaseSettings):
    LOG_FLOW: bool = True
    LOG_FLOW_CONSOLE: bool = True
    LOG_REQUESTS: bool = False
    LOG_DB: bool = True
    LOG_DB_CONSOLE: bool = True
    # LOG_MAX_BYTES: int = 10 * 1024 * 1024  # 10MB
    LOG_MAX_BYTES: int = 1 * 1024 * 1024  # 1MB
    LOG_BACKUP_COUNT: int = 3
    
    # add more logs if needed
    # SYS_LOG_ENABLED: bool = True
    # SYS_LOG_LEVEL: str = "INFO"
    

    # TODO: import from .env and also use Field(..., exclude=True) to prevent env binding
    # class Config:
    #     env_prefix = "LOG_"  # All vars will use LOG_ prefix in .env
    #     env_file = ".env"
    #     fields = {
    #         "LOG_BACKUP_COUNT": {"exclude": True}  # prevents env binding
    #     }

try:
    settings = LogSettings()
except ValidationError as e:
    import logging
    logging.basicConfig(level=logging.INFO)
    logging.warning(f"Invalid logging config, using defaults: {e}")
    settings = LogSettings()  # Fallback to defaults
