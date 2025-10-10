from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from bson.objectid import ObjectId

class User(BaseModel):
    username: str
    email: str
    hashed_password: str
    created_at: datetime
    is_verified: bool
    is_suspended: bool
    suspended_till: Optional[datetime]
    last_activity_at: datetime
    is_pending_deletion: bool
    delete_at: datetime

class UserOut(BaseModel):
    id: str
    hashed_password: str
    is_pending_deletion: bool
    is_suspended: bool
    is_verified: bool  