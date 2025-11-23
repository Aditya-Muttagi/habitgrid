from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=256, description="Plaintext password")

class UserRead(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime