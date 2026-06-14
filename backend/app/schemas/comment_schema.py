# backend/app/schemas/comment_schema.py
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class CommentCreate(BaseModel):
    user_id: int
    message: str

class CommentResponse(BaseModel):
    comment_id: int
    task_id: int
    user_id: int
    message: str
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)