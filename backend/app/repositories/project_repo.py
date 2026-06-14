# backend/app/repositories/project_repo.py
from sqlalchemy.orm import Session
from app.models.project import Project
from app.schemas.project_schema import ProjectCreate

def create_project(db: Session, project_data: ProjectCreate) -> Project:
    project = Project(
        name=project_data.name,
        description=project_data.description,
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project

def get_project_by_id(db: Session, project_id: int) -> Project | None:
    return db.query(Project).filter(Project.project_id == project_id).first()

def get_project_by_name(db: Session, name: str) -> Project | None:
    return db.query(Project).filter(Project.name == name).first()

def get_all_projects(db: Session) -> list[Project]:
    return db.query(Project).order_by(Project.project_id).all()