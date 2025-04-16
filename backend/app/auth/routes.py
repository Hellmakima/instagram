from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordBearer
from .utils import create_token, verify_token, create_refresh_token
from pydantic import BaseModel

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/token")
def login(data: LoginRequest, response: Response):
    # Replace this with your real user authentication logic
    access_token = create_token({"sub": data.username})
    refresh_token = create_refresh_token({"sub": data.username})
    
    # Set access token as HttpOnly cookie with SameSite and Secure flags
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,      # Can't access via JS
        secure=True,        # Only sent over HTTPS
        samesite="Strict",  # Or use "Lax" if more lenient behavior is needed
        max_age=60*60,      # Token expiration in seconds (1 hour)
    )
    
    # Optionally store the refresh token as a cookie too
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,      # Can't access via JS
        secure=True,        # Only sent over HTTPS
        samesite="Strict",  # Or use "Lax"
        max_age=60*60*24,   # Longer expiration for refresh token (1 day)
    )

    return {"message": "Login successful"}

class RefreshRequest(BaseModel):
    refresh_token: str

@router.post("/refresh")
def refresh(data: RefreshRequest, response: Response):
    payload = verify_token(data.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    # Create a new access token
    new_access = create_token({"sub": payload["sub"]})

    # Set the new access token as an HttpOnly cookie
    response.set_cookie(
        key="access_token",
        value=new_access,
        httponly=True,      # Can't access via JS
        secure=True,        # Only sent over HTTPS
        samesite="Strict",  # Or use "Lax" if more lenient behavior is needed
        max_age=60*60,      # Token expiration in seconds (1 hour)
    )

    return {
        "access_token": new_access,
        "token_type": "bearer"
    }

@router.get("/me")
def me(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"username": payload["sub"]}

# Optional: Logout route to delete cookies
@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Logged out successfully"}
