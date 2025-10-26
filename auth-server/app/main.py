# A'udhu billahi min ash-shaytan ir-rajim Bismillahi ar-Rahmani ar-Rahim

"""
### File: **app/main.py**

Contains the FastAPI app for the auth server
Collects all the routers from api folder and mounts them to the app
Manages the database connection

usage:
```bash
auth-server$ uv run uvicorn app.main:app --reload --port 5001
```
"""

import sys

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

import logging
from app.utils.loggers import init_loggers

try:
    init_loggers()
    security_logger = logging.getLogger("security_logger")
    security_logger.info("Attempting to start Auth Server.")
    from app.core.csrf import csrf_exception_handler, CsrfProtectError
    from app.core.lifespan import lifespan
    from app.api.router import router

    app = FastAPI(lifespan=lifespan, title="Auth Server", version="0.1")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://nmaa.com"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_exception_handler(CsrfProtectError, csrf_exception_handler)

    # Use an absolute path to the static directory so tests or VS Code runs from a
    # different working directory don't break finding the static files.
    from pathlib import Path
    static_dir = Path(__file__).resolve().parent / "static"
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    app.include_router(router)

    @app.get("/", include_in_schema=False)
    def root():
        return {"status": "ok"}

    security_logger.info("Auth Server started successfully.")

except Exception as e:
    # Avoid interactive prompts during test runs. Print the error and traceback
    # so CI/test runners can capture it.
    security_logger.error(f"Failed to start Auth Server: {str(e)}")
    print(f"\033[91mfailed to start server: {str(e)}\033[0m", file=sys.stderr)
    import traceback
    print(traceback.format_exc(), file=sys.stderr)
    print("Make sure your .env file is setup correctly and your database is running.")
    print("If you think this is a bug, please report it at \033[1;34mhttps://github.com/Hellmakima/instagram/issues\033[0m")
    sys.exit(1)