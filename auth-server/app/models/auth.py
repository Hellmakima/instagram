from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str
    hashed_password: str
    created_at: datetime
    is_verified: bool
    is_suspended: bool
    suspended_till: Optional[datetime]
    last_activity_at: datetime
    is_deleted: bool
    delete_at: datetime
    