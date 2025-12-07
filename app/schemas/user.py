from pydantic import BaseModel, EmailStr
from datetime import datetime

# Base Schema (Shared properties)
class UserBase(BaseModel):
    email: EmailStr

# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str
    full_name: str | None = None

# Properties to return to client (Never return password!)
class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    full_name: str | None = None

    class Config:
        # هذه السطر ضروري لكي يفهم Pydantic كائنات SQLAlchemy
        from_attributes = True