# backend/app/schemas/report_schema.py
from pydantic import BaseModel

class UserWorkloadReport(BaseModel):
    user_id: int
    user_name: str
    active_task_count: int

class ProjectProgressReport(BaseModel):
    project_id: int
    project_name: str
    total_tasks: int
    closed_tasks: int
    completion_percentage: float

class BlockedTaskReport(BaseModel):
    task_id: int
    title: str
    status: str
    blocking_task_id: int | None = None
    blocking_task_status: str | None = None