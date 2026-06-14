# backend/app/services/dependency_service.py
from sqlalchemy.orm import Session

from app.models.dependency import TaskDependency
from app.repositories import task_repo
from app.services import validation_service

def add_dependency(
    db: Session,
    task_id: int,
    depends_on_task_id: int,
) -> TaskDependency:
    validation_service.validate_dependency_can_be_created(
        db=db,
        task_id=task_id,
        depends_on_task_id=depends_on_task_id,
    )

    dependency = task_repo.create_dependency(
        db=db,
        task_id=task_id,
        depends_on_task_id=depends_on_task_id,
    )

    task_repo.insert_task_history(
        db=db,
        task_id=task_id,
        old_status=None,
        new_status="DEPENDENCY_ADDED",
        change_reason=f"Task now depends on task {depends_on_task_id}",
    )

    return dependency

def get_dependencies_for_task(db: Session, task_id: int) -> list:
    validation_service.ensure_task_exists(db, task_id)
    return task_repo.get_dependencies_for_task(db, task_id)