# backend/app/services/project_service.py
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.project import Project
from app.repositories import project_repo
from app.schemas.project_schema import ProjectCreate

def create_project(db: Session, project_data: ProjectCreate) -> Project:
    existing_project = project_repo.get_project_by_name(db, project_data.name)

    if existing_project is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Project with name {project_data.name} already exists",
        )

    return project_repo.create_project(db, project_data)

def get_project_by_id(db: Session, project_id: int) -> Project:
    project = project_repo.get_project_by_id(db, project_id)

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} does not exist",
        )

    return project

def get_all_projects(db: Session) -> list:
    return project_repo.get_all_projects(db)