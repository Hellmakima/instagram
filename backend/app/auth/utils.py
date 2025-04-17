from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
EXPIRE_MINUTES = 20
REFRESH_EXPIRE_DAYS = 7

def create_token(data: dict):
    data = data.copy()
    data["exp"] = datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)
    data["type"] = "access"  # ✅ mark token type
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    data = data.copy()
    data["exp"] = datetime.utcnow() + timedelta(days=REFRESH_EXPIRE_DAYS)
    data["type"] = "refresh"  # ✅ mark token type
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # caller must check "type"
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")