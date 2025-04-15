from datetime import datetime, timedelta
from jose import JWTError, jwt

SECRET_KEY = "super-secret"  # use dotenv or env vars in prod
ALGORITHM = "HS256"
EXPIRE_MINUTES = 60

def create_token(data: dict):
    data = data.copy()
    data["exp"] = datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
