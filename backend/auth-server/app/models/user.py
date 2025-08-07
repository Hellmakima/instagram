"""
### File: app/models/user.py

Contains the user model. Describe Database Schemas for backend DB server
I'm using it for data validation
"""
# from fastapi import HTTPException, status
# from pydantic import BaseModel, Field, field_validator
# from datetime import datetime, timezone
# import re
# from app.core.security import get_password_hash


# class UserBase(BaseModel):
#     # TODO: decide if username is all lowercase, and if it can include . _ -
#     username: str = Field(
#         ..., 
#         min_length=4, 
#         max_length=20, 
#         description="Username of the user"
#     )

#     @field_validator('username')
#     @classmethod
#     def validate_username_characters(cls, v: str) -> str:
#         # Allow only alphanumeric characters, periods, underscores, and hyphens.
#         if not re.match(r"^[a-zA-Z0-9._-]+$", v):
#             # Raise ValueError for Pydantic to catch and convert to 422
#             raise ValueError("Username must be alphanumeric and can include periods (.), underscores (_), and hyphens (-).")
#         return v

# class UserCreate(UserBase):
#     #TODO: id: str = Field(default=uuid.uuid4().hex, description="Unique ID of the user")
#     email: str = Field(..., description="Email of the user")
#     password: str = Field(..., description="Raw password (will be hashed)")
#     created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Timestamp of user creation")
#     is_verified: bool = False
#     is_blocked: bool = False
#     is_deleted: bool = False
    
#     async def doc(self):
#         return {
#             "username": self.username,
#             "hashed_password": await get_password_hash(self.password),
#             "created_at": self.created_at
#         }
    
#     @field_validator('email')
#     @classmethod
#     def validate_email_domain(cls, v: str) -> str:
#         if not v.endswith("@gmail.com"):
#             raise ValueError("We currently only support emails from the gmail.com domain.")
#         return v

#     @field_validator('password')
#     @classmethod
#     def validate_password_strength(cls, v: str) -> str:
#         MIN_PASSWORD_LENGTH = 10
#         MAX_PASSWORD_LENGTH = 72 # Common max length for password hashing algorithms

#         if len(v) < MIN_PASSWORD_LENGTH:
#             raise ValueError(f"Password must be at least {MIN_PASSWORD_LENGTH} characters long.")
#         if len(v) > MAX_PASSWORD_LENGTH:
#             raise ValueError(f"Password must be less than {MAX_PASSWORD_LENGTH} characters long.")
        
#         # Ensure complexity: at least one uppercase, one lowercase, one digit, one special character.
#         if not re.search(r'[A-Z]', v):
#             raise ValueError("Password must contain at least one uppercase letter.")
#         if not re.search(r'[a-z]', v):
#             raise ValueError("Password must contain at least one lowercase letter.")
#         if not re.search(r'\d', v):
#             raise ValueError("Password must contain at least one number.")
#         if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v): # Example special characters
#             raise ValueError("Password must contain at least one special character.")
            
#         return v

'''
class UserInDB(UserBase):
    # Model for users retrieved from the database
    # Assuming the database stores a unique ID (e.g., MongoDB's _id or a UUID)
    id: str = Field(..., alias="_id", description="Unique ID of the user in the database")
    email: EmailStr
    hashed_password: str
    created_at: datetime
    is_verified: bool
    is_blocked: bool
    is_deleted: bool

    class Config:
        populate_by_name = True # Allows Pydantic to use the alias for validation input

class UserUpdate(UserBase):
    # For updating user profiles, all fields should be optional.
    # Use Optional[Type] and default to None.
    username: Optional[str] = Field(
        None,
        min_length=4,
        max_length=20,
        description="New username of the user. Optional."
    )
    email: Optional[EmailStr] = Field(None, description="New email address of the user. Optional.")
    password: Optional[str] = Field(None, description="New raw password (will be hashed). Optional.")
    is_verified: Optional[bool] = None
    is_blocked: Optional[bool] = None
    is_deleted: Optional[bool] = None

    # Re-use password validation logic by calling the class method from UserCreate
    @field_validator('password')
    @classmethod
    def validate_optional_password_strength(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            # If a password is provided, validate its strength
            return UserCreate.validate_password_strength(v)
        return v

    @field_validator('email')
    @classmethod
    def validate_optional_email_domain(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            # If an email is provided, validate its domain
            return UserCreate.validate_email_domain(v)
        return v

    # Override username validator to be optional
    @field_validator('username')
    @classmethod
    def validate_optional_username_characters(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            return UserBase.validate_username_characters(v)
        return v

    async def to_db_doc(self) -> dict:
        update_data = {}
        if self.username is not None:
            update_data["username"] = self.username
        if self.email is not None:
            update_data["email"] = self.email
        if self.password is not None:
            update_data["hashed_password"] = await get_password_hash(self.password)
        if self.is_verified is not None:
            update_data["is_verified"] = self.is_verified
        if self.is_blocked is not None:
            update_data["is_blocked"] = self.is_blocked
        if self.is_deleted is not None:
            update_data["is_deleted"] = self.is_deleted
        return update_data

'''
