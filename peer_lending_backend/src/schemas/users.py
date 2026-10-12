# Pydantic models for the User entity #
# These models define the structure of user-related data for API requests and responses.

from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    full_name: str
    email: str
    phone: str

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True
