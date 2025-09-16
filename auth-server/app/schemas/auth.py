"""
### File: app/schemas/auth.py

Contains the auth incomming request schema. Describes JSON Structures for frontend requests.
"""

from pydantic import BaseModel, Field, field_validator, model_validator
import re

class UserCreate(BaseModel):
    # TODO: id: str = Field(default=uuid.uuid4().hex, description="Unique ID of the user")
    # TODO: decide if username is all lowercase, and if it can include . _ -
    username: str = Field(
        ..., 
        min_length=4, 
        max_length=20, 
        description="Username of the user"
    )
    email: str = Field(..., description="Email of the user")
    password: str = Field(
        ..., 
        min_length=10,
        max_length=72,
        description="Raw password (will be hashed)"
    )
    
    @field_validator('username')
    def validate_username_characters(cls, v: str) -> str:
        # Allow only alphanumeric characters, periods, underscores, and hyphens.
        if not re.match(r"^[a-zA-Z0-9._-]+$", v):
            # Raise ValueError for Pydantic to catch and convert to 422
            raise ValueError("Username must be alphanumeric and can include periods (.), underscores (_), and hyphens (-).")
        return v

    @field_validator('email')
    def validate_email_domain(cls, v: str) -> str:
        if not v.endswith("@gmail.com"):
            raise ValueError("We currently only support emails from the gmail.com domain.")
        return v

    @field_validator('password')
    def validate_password_strength(cls, v: str) -> str:
        # Ensure complexity: at least one uppercase, one lowercase, one digit, one special character.
        if not re.search(r'[A-Z]', v):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', v):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r'\d', v):
            raise ValueError("Password must contain at least one number.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v): # Example special characters
            raise ValueError("Password must contain at least one special character.")
        return v
    
    @model_validator(mode="after")
    def validate_password_similarity(self):
        # Ensure password does not contain username or email
        if self.username.lower() in self.password.lower():
            raise ValueError("Password must not contain the username.")
        if self.email.split("@")[0].lower() in self.password.lower():
            raise ValueError("Password must not contain the email name part.")
        return self
    
class LoginForm(BaseModel):
    username_or_email: str = Field(..., description="Username or email of the user")
    password: str = Field(..., description="Password of the user")

class TokenData(BaseModel):
    id: str = Field(..., description="Unique ID of the user")
