from pydantic import BaseModel

class AuthResponse(BaseModel):
    username: str
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"

class TokenData(BaseModel):
    username: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str 