# backend/app/schemas/task_schema.py
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class TaskCreate(BaseModel):
    project_id: int
    title: str
    description: str | None = None
    priority: str = "MEDIUM"

class TaskResponse(BaseModel):
    task_id: int
    project_id: int
    title: str
    description: str | None = None
    status: str
    priority: str
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)

class TaskStatusUpdate(BaseModel):
    new_status: str
    change_reason: str | None = None

class TaskAssignRequest(BaseModel):
    user_id: int

class TaskDependencyCreate(BaseModel):
    depends_on_task_id: int

class TaskHistoryResponse(BaseModel):
    history_id: int
    task_id: int
    old_status: str | None = None
    new_status: str
    change_reason: str | None = None
    changed_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)

class TaskDependencyResponse(BaseModel):
    dependency_id: int
    task_id: int
    depends_on_task_id: int

    model_config = ConfigDict(from_attributes=True)