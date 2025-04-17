from fastapi import APIRouter, HTTPException, Response, Request
from pydantic import BaseModel
from .utils import create_token, verify_token

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/token")
def login(data: LoginRequest, response: Response):
    # Simulate user check here
    access = create_token({"sub": data.username})
    refresh = create_token({"sub": data.username}, is_refresh=True)

    cookie_opts = {
        "httponly": True,
        "secure": True,
        "samesite": "Lax",
        "path": "/",
    }

    response.set_cookie("access_token", access, max_age=60 * 60, **cookie_opts)
    response.set_cookie("refresh_token", refresh, max_age=60 * 60 * 24, **cookie_opts)

    return {"message": "Login successful"}

@router.post("/refresh")
def refresh(request: Request, response: Response):
    token = request.cookies.get("refresh_token")
    payload = verify_token(token)

    if payload.get("type") != "refresh":
        raise HTTPException(401, "Invalid refresh token")

    new_access_token = create_token({"sub": payload["sub"]})

    response.set_cookie(
        "access_token", new_access_token, max_age=60 * 60, httponly=True, secure=True, samesite="Lax", path="/"
    )

    return {"message": "Token refreshed"}

@router.get("/me")
def me(request: Request):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(401, "Not logged in")

    payload = verify_token(access_token)
    if payload.get("type") != "access":
        raise HTTPException(401, "Wrong token type")

    return {"user": payload["sub"]}

@router.post("/logout")
def logout(response: Response):
    for name in ["access_token", "refresh_token"]:
        response.delete_cookie(name, path="/")
    return {"message": "Logged out"}
