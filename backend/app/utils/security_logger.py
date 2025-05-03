import logging
from logging.config import dictConfig
from app.core.config import settings
# DEBUG < INFO < WARNING < ERROR < CRITICAL
LOG_CONFIG = {
    "version": 1,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
        },
    },
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "filename": "app.log",
            "formatter": "default",
            "level": "INFO",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "INFO",
        },
    },
    "root": {
        "handlers": ["file", "console"],
        "level": "INFO",
    },
}

dictConfig(LOG_CONFIG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
