from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.auth import routes as auth_routes

app = FastAPI()

app.include_router(auth_routes.router, prefix="/auth")

app.mount("/", StaticFiles(directory="app/static", html=True), name="static")


# uvicorn main:app --reload --port 5000
# uvicorn app.main:app --reload --port 5000