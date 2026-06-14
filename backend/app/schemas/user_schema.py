# backend/app/schemas/user_schema.py
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    role: str = "USER"
    max_active_tasks: int = 3

class UserResponse(BaseModel):
    user_id: int
    name: str
    email: str
    role: str
    max_active_tasks: int
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
