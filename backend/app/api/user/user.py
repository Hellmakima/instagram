from fastapi import APIRouter, Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# from fastapi.encoders import jsonable_encoder
# from sqlalchemy.orm import Session
from app.core.security import get_password_hash, verify_password
# from app.core.config import settings
from app.core.db import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

router = APIRouter()

# implemet the token stuff here and also in security.py
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# @router.post("/register", response_model=User)
# def register_user(user: UserCreate, db: Session = Depends(get_db)):
#     db_user = db.query(User).filter(User.email == user.email).first()
#     if db_user:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Email already registered"
#         )
#     hashed_password = get_password_hash(user.password)
#     db_user = User(email=user.email, hashed_password=hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# @router.post("/login", response_model=User)
# def login_user(user: UserCreate, db: Session = Depends(get_db), response):
#     db_user = db.query(User).filter(User.email == user.email).first()
#     if not db_user:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Incorrect email or password"
#         )
#     if not verify_password(user.password, db_user.hashed_password):
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Incorrect email or password"
#         )
#     access_token = response.access_token
#     return {"access_token": access_token, "token_type": "bearer"}