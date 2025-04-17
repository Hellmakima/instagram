from fastapi import APIRouter, Depends, HTTPException, Response, Request
from .utils import create_token, verify_token, create_refresh_token
from pydantic import BaseModel

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/token")
def login(data: LoginRequest, response: Response, request: Request):
    print("Sending cookies:", response.headers)
    # Simulated authentication (replace with real check)
    access_token = create_token({"sub": data.username})
    refresh_token = create_refresh_token({"sub": data.username})

    domain = request.url.hostname  # dynamic domain for portability

    cookie_settings = {
        "httponly": True,
        "secure": True,
        "samesite": "None",
        "domain": domain,
        "path": "/",
    }

    response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=60 * 60,
        **cookie_settings
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=60 * 60 * 24,
        **cookie_settings
    )

    return {"message": "Login successful"}

@router.post("/refresh")
def refresh(response: Response, request: Request):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    payload = verify_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_access = create_token({"sub": payload["sub"]})

    domain = request.url.hostname

    response.set_cookie(
        key="access_token",
        value=new_access,
        max_age=60 * 60,
        httponly=True,
        secure=True,
        samesite="None",
        domain=domain,
        path="/",
    )

    return {"access_token": new_access, "token_type": "bearer"}

@router.get("/me")
def me(request: Request):
    print("In ME:", request.cookies)
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Missing token")

    payload = verify_token(access_token)
    if not payload or payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Invalid or wrong token")

    return {"username": payload["sub"]}

@router.post("/logout")
def logout(response: Response, request: Request):
    domain = request.url.hostname
    response.delete_cookie("access_token", domain=domain, path="/")
    response.delete_cookie("refresh_token", domain=domain, path="/")
    return {"message": "Logged out successfully"}
