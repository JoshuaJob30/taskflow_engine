# backend/app/routes/project_routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.project_schema import ProjectCreate, ProjectResponse
from app.schemas.task_schema import TaskResponse
from app.services import project_service, task_service

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)

@router.post("", response_model=ProjectResponse)
def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
):
    return project_service.create_project(db, project_data)

@router.get("", response_model=list[ProjectResponse])
def get_all_projects(
    db: Session = Depends(get_db),
):
    return project_service.get_all_projects(db)

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project_by_id(
    project_id: int,
    db: Session = Depends(get_db),
):
    return project_service.get_project_by_id(db, project_id)

@router.get("/{project_id}/tasks", response_model=list[TaskResponse])
def get_tasks_by_project(
    project_id: int,
    db: Session = Depends(get_db),
):
    return task_service.get_tasks_by_project(db, project_id)