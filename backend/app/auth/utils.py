import os
import secrets
from datetime import datetime, timedelta
from fastapi import HTTPException, Request
from fastapi.responses import HTMLResponse
from jose import jwt, JWTError

SECRET_KEY = os.getenv("SECRET_KEY", "secret")
CSRF_SECRET_KEY = os.getenv("CSRF_SECRET_KEY", "csrf_secret")
ALGORITHM = "HS256"
ACCESS_EXPIRE_MINUTES = 60  # 1 hour
REFRESH_EXPIRE_DAYS = 7


def generate_csrf_token() -> str:
    """Generate a random CSRF token."""
    return secrets.token_urlsafe(32)

def verify_csrf_token(csrf_token: str, request: Request) -> bool:
    """Verify the CSRF token sent in the request."""
    cookie_csrf_token = request.cookies.get("csrf_token")
    if not cookie_csrf_token:
        raise HTTPException(status_code=400, detail="CSRF token missing")
    
    if csrf_token != cookie_csrf_token:
        raise HTTPException(status_code=403, detail="Invalid CSRF token")
    
    return True


def create_token(data: dict, is_refresh=False):
    data = data.copy()
    if is_refresh:
        data["exp"] = datetime.utcnow() + timedelta(days=REFRESH_EXPIRE_DAYS)
        data["type"] = "refresh"
    else:
        data["exp"] = datetime.utcnow() + timedelta(minutes=ACCESS_EXPIRE_MINUTES)
        data["type"] = "access"
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str, token_type: str = None):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if token_type and payload.get("type") != token_type:
            raise HTTPException(status_code=401, detail="Invalid token type")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

