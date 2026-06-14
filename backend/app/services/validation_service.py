# backend/app/services/validation_service.py
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.task import Task
from app.models.user import User
from app.models.project import Project
from app.repositories import task_repo, user_repo, project_repo
from app.utils.constants import (
    VALID_STATUS_TRANSITIONS,
    TASK_STATUS_CREATED,
    TASK_STATUS_ASSIGNED,
    TASK_STATUS_IN_PROGRESS,
    TASK_STATUS_BLOCKED,
    TASK_STATUS_RESOLVED,
    TASK_STATUS_CLOSED,
)

def ensure_task_exists(db: Session, task_id: int) -> Task:
    task = task_repo.get_task_by_id(db, task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} does not exist",
        )

    return task

def ensure_user_exists(db: Session, user_id: int) -> User:
    user = user_repo.get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} does not exist",
        )

    return user

def ensure_project_exists(db: Session, project_id: int) -> Project:
    project = project_repo.get_project_by_id(db, project_id)

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} does not exist",
        )

    return project

def ensure_task_is_not_closed(task: Task) -> None:
    if task.status == TASK_STATUS_CLOSED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Closed tasks cannot be modified",
        )

def validate_status_transition(current_status: str, new_status: str) -> None:
    allowed_next_statuses = VALID_STATUS_TRANSITIONS.get(current_status, [])

    if new_status not in allowed_next_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Invalid status transition from {current_status} to {new_status}. "
                f"Allowed transitions: {allowed_next_statuses}"
            ),
        )

def validate_assignment_required_for_progress(db: Session, task_id: int, new_status: str) -> None:
    if new_status != TASK_STATUS_IN_PROGRESS:
        return

    assignment = task_repo.get_assignment_by_task_id(db, task_id)

    if assignment is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task must be assigned before it can move to IN_PROGRESS",
        )

def validate_dependencies_resolved_for_progress(
    db: Session,
    task_id: int,
    new_status: str,
) -> None:
    if new_status != TASK_STATUS_IN_PROGRESS:
        return

    unresolved_dependencies = task_repo.get_unresolved_dependencies(db, task_id)

    if unresolved_dependencies:
        unresolved_ids = [task.task_id for task in unresolved_dependencies]

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Task cannot move to IN_PROGRESS because dependent tasks are unresolved. "
                f"Unresolved dependency task ids: {unresolved_ids}"
            ),
        )

def validate_user_workload_limit(db: Session, user: User) -> None:
    active_task_count = task_repo.count_active_tasks_for_user(db, user.user_id)

    if active_task_count >= user.max_active_tasks:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"User {user.user_id} already has {active_task_count} active tasks. "
                f"Maximum allowed active tasks: {user.max_active_tasks}"
            ),
        )

def validate_task_can_be_assigned(db: Session, task: Task, user: User) -> None:
    ensure_task_is_not_closed(task)
    validate_user_workload_limit(db, user)

def validate_task_can_change_status(
    db: Session,
    task: Task,
    new_status: str,
) -> None:
    ensure_task_is_not_closed(task)

    validate_status_transition(
        current_status=task.status,
        new_status=new_status,
    )

    validate_assignment_required_for_progress(
        db=db,
        task_id=task.task_id,
        new_status=new_status,
    )

    validate_dependencies_resolved_for_progress(
        db=db,
        task_id=task.task_id,
        new_status=new_status,
    )

def validate_dependency_not_self(task_id: int, depends_on_task_id: int) -> None:
    if task_id == depends_on_task_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A task cannot depend on itself",
        )

def validate_dependency_not_duplicate(
    db: Session,
    task_id: int,
    depends_on_task_id: int,
) -> None:
    existing_dependency = task_repo.get_dependency_between_tasks(
        db=db,
        task_id=task_id,
        depends_on_task_id=depends_on_task_id,
    )

    if existing_dependency is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Dependency already exists: task {task_id} already depends on "
                f"task {depends_on_task_id}"
            ),
        )

def validate_dependency_can_be_created(
    db: Session,
    task_id: int,
    depends_on_task_id: int,
) -> tuple[Task, Task]:
    task = ensure_task_exists(db, task_id)
    depends_on_task = ensure_task_exists(db, depends_on_task_id)

    ensure_task_is_not_closed(task)

    validate_dependency_not_self(
        task_id=task_id,
        depends_on_task_id=depends_on_task_id,
    )

    validate_dependency_not_duplicate(
        db=db,
        task_id=task_id,
        depends_on_task_id=depends_on_task_id,
    )

    return task, depends_on_task