from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.auth import routes as auth_routes

app = FastAPI()

# Including authentication routes with /auth prefix
app.include_router(auth_routes.router, prefix="/auth")

# Mount static files from app/static, serving as a single-page app (SPA) or assets
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")

# uvicorn main:app --reload --port 5000
# uvicorn app.main:app --reload --port 5000
