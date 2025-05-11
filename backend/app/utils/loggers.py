"""
### File: **app/core/loggers.py**

Contains the loggers of the project.
Settings are loaded from logging_config.py

to use loggers:
```
from logging import getLogger
logger = getLogger(__name__) 
# replace __name__ with the name of the logger defined in loggers.py

logger.info("info")
logger.warning("warning")
logger.error("error")
```
"""

import logging
from logging.config import dictConfig
from app.core.logging_config import settings
import os
 

"""
logging levels:
    NONSET < DEBUG < INFO < WARNING < ERROR < CRITICAL 
    these are like enums. putting values like CRITICAL + 1 will not log anything.

in formatters:
    %(asctime)s - Time in format: 2023-05-03 16:21:00
    %(name)s - Name of the logger
    %(levelname)s - Level of the logger (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    %(message)s - Message of the logger
    %(module)s - Name of the python module
    %(process)d - Process ID
"""

os.makedirs('logs', exist_ok=True)

LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False, # Preserve existing loggers

    "formatters": {
        "default": {
            # used by other modules/libraries used.
            "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s; default log"
        },
        "request": {
            # to track any request
            "format": "[%(asctime)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "verbose": { 
            # detailed log
            "format": "[%(asctime)s] [%(process)d] [%(name)s] [%(levelname)s] in %(module)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "flow": {
            # to track stack trace
            "format": "[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        # "json": {
        #     # TODO for future use (mostly security)
        #     # json log example
        #     # {"asctime": "2025-05-04 12:34:56,789", "name": "app", "levelname": "WARNING", "message": "Disk space low"}
        #     "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
        #     "fmt": "%(asctime)s %(name)s %(levelname)s %(message)s"
        # }
    },
    
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            "level": "INFO"
        },
        "security_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/security.log",
            "formatter": "verbose",
            "encoding": "utf-8",
            "backupCount": settings.LOG_BACKUP_COUNT,
            "maxBytes": settings.LOG_MAX_BYTES,
            "level": "INFO"
        },
        "request_console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            "level": "INFO"
        },
        "flow_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/flow.log",
            "formatter": "verbose",
            "encoding": "utf-8",
            "backupCount": settings.LOG_BACKUP_COUNT,
            "maxBytes": settings.LOG_MAX_BYTES,
            "level": "DEBUG"
        },
        "db_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/db.log",
            "formatter": "verbose",
            "encoding": "utf-8",
            "backupCount": settings.LOG_BACKUP_COUNT,
            "maxBytes": settings.LOG_MAX_BYTES,
            "level": "DEBUG"
        }
    },
    
    "loggers": {
        "security_logger": {
            "handlers": ["security_file"],
            "level": "INFO",
            "propagate": False # Don't send to root logger
        },
        "app_requests": {
            # TODO: this is to use when tracking varying IP addresses. not useful rn
            "handlers": ["request_console"],
            "level": "INFO",
            "propagate": False
        },
        "app_flow": {
            "handlers": ["flow_file", "console"] if settings.LOG_FLOW_CONSOLE else ["flow_file"],
            "level": "DEBUG" if settings.LOG_FLOW else "CRITICAL",
            "propagate": False
        },
        "app_db": {
            "handlers": ["db_file", "console"] if settings.LOG_DB_CONSOLE else ["db_file"],
            "level": "DEBUG" if settings.LOG_DB else "CRITICAL",
            "propagate": False
        }
    },
    
    "root": {
        # Fallback
        "handlers": ["console"],
        "level": "WARNING" # Only capture warnings+ from unhandled logs
    }
}

# Configure log levels based on settings
if not settings.LOG_FLOW:
    LOG_CONFIG["loggers"]["app_flow"]["level"] = logging.CRITICAL + 1
if not settings.LOG_FLOW_CONSOLE:
    LOG_CONFIG["loggers"]["app_flow"]["handlers"].remove("console")
if not settings.LOG_REQUESTS:
    LOG_CONFIG["loggers"]["app_requests"]["level"] = logging.CRITICAL + 1
if not settings.LOG_DB:
    LOG_CONFIG["loggers"]["app_db"]["level"] = logging.CRITICAL + 1
if not settings.LOG_DB_CONSOLE:
    LOG_CONFIG["loggers"]["app_db"]["handlers"].remove("console")

# Try to add JSON formatter if python-json-logger is available
try:
    from pythonjsonlogger import jsonlogger
    LOG_CONFIG["formatters"]["json"] = {
        "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
        "fmt": "%(asctime)s %(name)s %(levelname)s %(message)s"
    }
    LOG_CONFIG["handlers"]["security_file"]["formatter"] = "json"  # Use JSON if available
except ImportError:
    # If python-json-logger is missing, fall back to 'verbose' for security logs
    import warnings
    warnings.warn(
        "python-json-logger not installed. Security logs will use verbose (plaintext) formatting. " 
        "Install with: pip install python-json-logger"
    )
    LOG_CONFIG["handlers"]["security_file"]["formatter"] = "verbose"

dictConfig(LOG_CONFIG)
    
"""
# Can add color to logs
pip install colorlog
"formatters": {
    "colorful": {
        "()": "colorlog.ColoredFormatter",
        "format": "%(log_color)s[%(asctime)s] [%(levelname)s] in %(module)s: %(message)s",
        "datefmt": "%Y-%m-%d %H:%M:%S",
        "log_colors": {
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        }
    },
    # other formatters...
}


# All this can also be done manually
logger = logging.getLogger(__name__)
logger = logging.getLogger('app.flow')
logger.setLevel(logging.INFO)

# # 1. System/Operational Logs (Infrastructure-level)
sys_logger = getLogger("sys")  # Or "ops" for operations

# # 2. Request/Endpoint Logs (API traffic)
# request_logger = getLogger("http")  # More standard than "endpoint_logger"

if not settings.LOG_FLOW_ENABLED:
    LOG_CONFIG["loggers"]["app.flow"]["level"] = 51

if settings.SYS_LOG_ENABLED:
    sys_logger.setLevel(settings.SYS_LOG_LEVEL)
    sys_logger.addHandler(logging.FileHandler(f"{settings.LOG_DIR}/sys.log"))
    sys_logger.addHandler(logging.StreamHandler())
else:
    sys_logger.addHandler(logging.NullHandler())
"""

