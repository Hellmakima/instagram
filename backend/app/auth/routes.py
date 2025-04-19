from fastapi import APIRouter, HTTPException, Response, Request
from pydantic import BaseModel
from .utils import create_token, verify_token, generate_csrf_token, verify_csrf_token

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/token")
def login(data: LoginRequest, response: Response, request: Request):
    # Verify CSRF token
    # csrf_token = request.headers.get("X-CSRF-Token")
    # verify_csrf_token(csrf_token, request)
    
    # Simulate user check here 
    #TODO add verification of username and password

    access = create_token({"sub": data.username})
    response.set_cookie(
        "access_token",
        access,
        httponly=True,
        secure=True,
        samesite="Strict",
        path="/",
        max_age=60 * 15  # 15 minutes
    )

    refresh = create_token({"sub": data.username}, is_refresh=True)
    response.set_cookie(
        "refresh_token",
        refresh,
        httponly=True,
        secure=True,
        samesite="Strict",
        path="/",
        max_age=60 * 60 * 24  # 24 hours
    )

    csrf_token = generate_csrf_token()
    # Set CSRF token cookie without HttpOnly
    response.set_cookie(
        "csrf_token",
        csrf_token,
        secure=True,
        samesite="Strict",  # Or "Lax"
        path="/",
        max_age=60 * 60 * 24
    )

    return {"message": "Login successful"}


@router.post("/refresh")
def refresh(request: Request, response: Response):
    csrf_token = request.headers.get("X-CSRF-Token")
    verify_csrf_token(csrf_token, request)

    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(401, "No refresh token found")

    # Verify the refresh token
    payload = verify_token(token, "refresh")

    # Generate a new access token
    new_access_token = create_token({"sub": payload["sub"]})


    # Set the new tokens as cookies
    cookie_opts = {
        "httponly": True,
        "secure": True,
        "samesite": "Lax",
        "path": "/",
    }
    
    # Set new tokens in cookies
    response.set_cookie("access_token", new_access_token, max_age=60 * 60, **cookie_opts)
    # # Optionally, generate a new refresh token (rotate it)
    # new_refresh_token = create_token({"sub": payload["sub"]}, is_refresh=True)
    # response.set_cookie("refresh_token", new_refresh_token, max_age=60 * 60 * 24, **cookie_opts)

    return {"message": "Token refreshed"}


@router.get("/me")
def me(request: Request):
    
    # csrf_token = request.headers.get("X-CSRF-Token")
    # verify_csrf_token(csrf_token, request)

    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(401, "Not logged in")

    payload = verify_token(access_token)
    if payload.get("type") != "access":
        raise HTTPException(401, "Wrong token type")

    return {"user": payload["sub"]}

@router.post("/logout")
def logout(response: Response, request: Request):
    # Verify CSRF token
    csrf_token = request.headers.get("X-CSRF-Token")
    print(csrf_token)
    verify_csrf_token(csrf_token, request)
    
    for name in ["access_token", "refresh_token", "csrf_token"]:
        response.delete_cookie(name, path="/")
    return {"message": "Logged out"}
