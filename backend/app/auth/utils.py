from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException


SECRET_KEY = "super-super-secret"  # use dotenv or env vars in prod
ALGORITHM = "HS256"
EXPIRE_MINUTES = 20
REFRESH_EXPIRE_DAYS = 7

def create_refresh_token(data: dict):
    data = data.copy()
    # data["exp"] = datetime.now(datetime.timezone.utc) + timedelta(days=REFRESH_EXPIRE_DAYS)
    data["exp"] = datetime.utcnow() + timedelta(days=REFRESH_EXPIRE_DAYS)
    data["type"] = "refresh"
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def create_token(data: dict):
    data = data.copy()
    # data["exp"] = datetime.now(datetime.timezone.utc) + timedelta(minutes=EXPIRE_MINUTES)
    data["exp"] = datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid token")
