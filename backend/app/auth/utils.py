from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException
import os

SECRET_KEY = os.getenv("SECRET_KEY", "secret")
ALGORITHM = "HS256"
ACCESS_EXPIRE_MINUTES = 60  # 1 hour
REFRESH_EXPIRE_DAYS = 7

def create_token(data: dict, is_refresh=False):
    data = data.copy()
    if is_refresh:
        data["exp"] = datetime.utcnow() + timedelta(days=REFRESH_EXPIRE_DAYS)
        data["type"] = "refresh"
    else:
        data["exp"] = datetime.utcnow() + timedelta(minutes=ACCESS_EXPIRE_MINUTES)
        data["type"] = "access"
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # caller must check "type"
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
