# backend/app/services/task_service.py
from sqlalchemy.orm import Session

from app.models.task import Task
from app.models.assignment import TaskAssignment
from app.models.comment import Comment
from app.models.history import TaskHistory
from app.schemas.task_schema import TaskCreate, TaskStatusUpdate
from app.schemas.comment_schema import CommentCreate
from app.repositories import task_repo
from app.services import validation_service
from app.utils.constants import TASK_STATUS_CREATED, TASK_STATUS_ASSIGNED

def create_task(db: Session, task_data: TaskCreate) -> Task:
    validation_service.ensure_project_exists(db, task_data.project_id)

    task = task_repo.create_task(db, task_data)

    task_repo.insert_task_history(
        db=db,
        task_id=task.task_id,
        old_status=None,
        new_status=TASK_STATUS_CREATED,
        change_reason="Task created",
    )

    return task

def get_task_by_id(db: Session, task_id: int) -> Task:
    return validation_service.ensure_task_exists(db, task_id)

def get_all_tasks(db: Session) -> list[Task]:
    return task_repo.get_all_tasks(db)

def get_tasks_by_project(db: Session, project_id: int) -> list[Task]:
    validation_service.ensure_project_exists(db, project_id)
    return task_repo.get_tasks_by_project(db, project_id)

def assign_task(db: Session, task_id: int, user_id: int) -> TaskAssignment:
    task = validation_service.ensure_task_exists(db, task_id)
    user = validation_service.ensure_user_exists(db, user_id)

    validation_service.validate_task_can_be_assigned(
        db=db,
        task=task,
        user=user,
    )

    assignment = task_repo.assign_task_to_user(
        db=db,
        task_id=task_id,
        user_id=user_id,
    )

    if task.status == TASK_STATUS_CREATED:
        old_status = task.status

        task_repo.update_task_status(
            db=db,
            task=task,
            new_status=TASK_STATUS_ASSIGNED,
        )

        task_repo.insert_task_history(
            db=db,
            task_id=task_id,
            old_status=old_status,
            new_status=TASK_STATUS_ASSIGNED,
            change_reason=f"Task assigned to user {user_id}",
        )

    return assignment

def update_task_status(
    db: Session,
    task_id: int,
    status_update: TaskStatusUpdate,
) -> Task:
    task = validation_service.ensure_task_exists(db, task_id)

    old_status = task.status
    new_status = status_update.new_status

    validation_service.validate_task_can_change_status(
        db=db,
        task=task,
        new_status=new_status,
    )

    updated_task = task_repo.update_task_status(
        db=db,
        task=task,
        new_status=new_status,
    )

    task_repo.insert_task_history(
        db=db,
        task_id=task_id,
        old_status=old_status,
        new_status=new_status,
        change_reason=status_update.change_reason,
    )

    return updated_task

def add_comment(
    db: Session,
    task_id: int,
    comment_data: CommentCreate,
) -> Comment:
    task = validation_service.ensure_task_exists(db, task_id)
    validation_service.ensure_task_is_not_closed(task)
    validation_service.ensure_user_exists(db, comment_data.user_id)

    return task_repo.add_comment(
        db=db,
        task_id=task_id,
        comment_data=comment_data,
    )

def get_comments_for_task(db: Session, task_id: int) -> list[Comment]:
    validation_service.ensure_task_exists(db, task_id)
    return task_repo.get_comments_for_task(db, task_id)

def get_task_history(db: Session, task_id: int) -> list[TaskHistory]:
    validation_service.ensure_task_exists(db, task_id)
    return task_repo.get_task_history(db, task_id)