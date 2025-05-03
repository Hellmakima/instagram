# app/utils/logger.py

import logging

from dotenv import load_dotenv
load_dotenv()

from app.core.config import settings

logger = logging.getLogger("flow_logger")

if settings.ENABLE_APP_LOGGER:
    logger.setLevel(logging.DEBUG)
    
    # console_handler = logging.StreamHandler()
    # formatter = logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
    # console_handler.setFormatter(formatter)

    # if not logger.hasHandlers():
    #     logger.addHandler(console_handler)

    file_handler = logging.FileHandler("flow.log", mode="a", encoding="utf-8")
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
    file_handler.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(file_handler)
else:
    logger.addHandler(logging.NullHandler())
