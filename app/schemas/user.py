from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# ---- Base ----
class UserBase(BaseModel):
    username: str = Field(..., max_length=50)
    email: EmailStr
    full_name: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False

# ---- Create (includes plaintext password) ----
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128)

# ---- Update ----
class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=8, max_length=128)

# ---- Outbound / Response ----
class UserOut(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # SQLAlchemy -> Pydantic
