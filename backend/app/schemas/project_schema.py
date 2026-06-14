# backend/app/schemas/project_schema.py
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class ProjectCreate(BaseModel):
    name: str
    description: str | None = None

class ProjectResponse(BaseModel):
    project_id: int
    name: str
    description: str | None = None
    created_at: datetime | None