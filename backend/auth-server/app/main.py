# A'udhu billahi min ash-shaytan ir-rajim Bismillahi ar-Rahmani ar-Rahim

"""
### File: **app/main.py**

Contains the FastAPI app for the auth server
Collects all the routers from api folder and mounts them to the app
Manages the database connection

to run the app in /backend> uvicorn app.main:app --reload --port 5000
or hit f5 in vscode
"""

# mongodb connection client
from fastapi.staticfiles import StaticFiles
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

# fastapi app
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import request_validation_exception_handler

# csrf protection
from app.core.csrf import csrf_exception_handler, CsrfProtectError
from app.api.api_v1.router import router

# startup
from contextlib import asynccontextmanager
import app.utils.loggers # initialize loggers

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    app.state.client = client
    
    await app.state.client.admin.command("ping")
    # TODO: Create indexes for all collections
    db = client.get_database()
    
    # this should be done only once.
    # await db.users.create_index("username", unique=True)
    
    yield
    client.close()

app = FastAPI(lifespan=lifespan, title="Auth Server", version="0.1")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.add_exception_handler(CsrfProtectError, csrf_exception_handler)

# TODO: remove this
# from fastapi.responses import FileResponse
# from fastapi.requests import Request
# from starlette.exceptions import HTTPException as StarletteHTTPException

# @app.exception_handler(StarletteHTTPException)
# async def custom_404_handler(request: Request, exc: StarletteHTTPException):
#     if exc.status_code == 404:
#         return FileResponse("app/static/index.html")
#     raise exc

# TODO: remove this
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import status, Request
from app.schemas.auth import (
    APIErrorResponse,
    ErrorDetail,
)
from pydantic import ValidationError
# This is the custom exception handler. It catches all RequestValidationError instances.
@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Your custom logic to extract and format the error details
    error_detail = exc.errors()[0]  # Get the first validation error
    loc = ".".join(map(str, error_detail["loc"]))
    msg = error_detail["msg"]

    # Construct your custom error response
    response_body = APIErrorResponse(
        message=f"Validation failed for field: {loc}",
        error=ErrorDetail(
            code="VALIDATION_ERROR",
            details=f"An error occurred: {msg}"
        )
    )

    # Return a JSONResponse with your custom body and the 422 status code
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(response_body),
    )

app.include_router(router)