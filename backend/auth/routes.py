from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Placeholder logic, replace with real checks
    if form_data.username == "admin" and form_data.password == "secret":
        return {"access_token": "fake-token", "token_type": "bearer"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

@router.get("/me")
def read_user(token: str = Depends(oauth2_scheme)):
    # Placeholder logic, replace with real checks
    return {"username": "admin"}