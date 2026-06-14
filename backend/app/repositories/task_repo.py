# backend/app/repositories/task_repo.py
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.task import Task
from app.models.assignment import TaskAssignment
from app.models.dependency import TaskDependency
from app.models.history import TaskHistory
from app.models.comment import Comment
from app.schemas.task_schema import TaskCreate
from app.schemas.comment_schema import CommentCreate
from app.utils.constants import ACTIVE_STATUSES

def create_task(db: Session, task_data: TaskCreate) -> Task:
    task = Task(
        project_id=task_data.project_id,
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        status="CREATED",
    )

    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_task_by_id(db: Session, task_id: int) -> Task | None:
    return db.query(Task).filter(Task.task_id == task_id).first()

def get_all_tasks(db: Session) -> list[Task]:
    return db.query(Task).order_by(Task.task_id).all()

def get_tasks_by_project(db: Session, project_id: int) -> list[Task]:
    return (
        db.query(Task)
        .filter(Task.project_id == project_id)
        .order_by(Task.task_id)
        .all()
    )

def update_task_status(db: Session, task: Task, new_status: str) -> Task:
    task.status = new_status
    task.updated_at = datetime.now(timezone.utc)

    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_assignment_by_task_id(db: Session, task_id: int) -> TaskAssignment | None:
    return (
        db.query(TaskAssignment)
        .filter(TaskAssignment.task_id == task_id)
        .first()
    )

def assign_task_to_user(db: Session, task_id: int, user_id: int) -> TaskAssignment:
    existing_assignment = get_assignment_by_task_id(db, task_id)

    if existing_assignment:
        existing_assignment.user_id = user_id
        db.add(existing_assignment)
        db.commit()
        db.refresh(existing_assignment)
        return existing_assignment

    assignment = TaskAssignment(
        task_id=task_id,
        user_id=user_id,
    )

    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment

def get_assignments_by_user_id(db: Session, user_id: int) -> list[TaskAssignment]:
    return (
        db.query(TaskAssignment)
        .filter(TaskAssignment.user_id == user_id)
        .all()
    )

def count_active_tasks_for_user(db: Session, user_id: int) -> int:
    return (
        db.query(Task)
        .join(TaskAssignment, Task.task_id == TaskAssignment.task_id)
        .filter(TaskAssignment.user_id == user_id)
        .filter(Task.status.in_(ACTIVE_STATUSES))
        .count()
    )

def create_dependency(
    db: Session,
    task_id: int,
    depends_on_task_id: int,
) -> TaskDependency:
    dependency = TaskDependency(
        task_id=task_id,
        depends_on_task_id=depends_on_task_id,
    )

    db.add(dependency)
    db.commit()
    db.refresh(dependency)
    return dependency

def get_dependencies_for_task(db: Session, task_id: int) -> list[TaskDependency]:
    return (
        db.query(TaskDependency)
        .filter(TaskDependency.task_id == task_id)
        .all()
    )

def get_dependency_between_tasks(
    db: Session,
    task_id: int,
    depends_on_task_id: int,
) -> TaskDependency | None:
    return (
        db.query(TaskDependency)
        .filter(TaskDependency.task_id == task_id)
        .filter(TaskDependency.depends_on_task_id == depends_on_task_id)
        .first()
    )

def get_unresolved_dependencies(db: Session, task_id: int) -> list[Task]:
    return (
        db.query(Task)
        .join(
            TaskDependency,
            Task.task_id == TaskDependency.depends_on_task_id,
        )
        .filter(TaskDependency.task_id == task_id)
        .filter(Task.status != "RESOLVED")
        .all()
    )

def insert_task_history(
    db: Session,
    task_id: int,
    old_status: str | None,
    new_status: str,
    change_reason: str | None = None,
) -> TaskHistory:
    history = TaskHistory(
        task_id=task_id,
        old_status=old_status,
        new_status=new_status,
        change_reason=change_reason,
    )

    db.add(history)
    db.commit()
    db.refresh(history)
    return history

def get_task_history(db: Session, task_id: int) -> list[TaskHistory]:
    return (
        db.query(TaskHistory)
        .filter(TaskHistory.task_id == task_id)
        .order_by(TaskHistory.changed_at)
        .all()
    )

def add_comment(
    db: Session,
    task_id: int,
    comment_data: CommentCreate,
) -> Comment:
    comment = Comment(
        task_id=task_id,
        user_id=comment_data.user_id,
        message=comment_data.message,
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

def get_comments_for_task(db: Session, task_id: int) -> list[Comment]:
    return (
        db.query(Comment)
        .filter(Comment.task_id == task_id)
        .order_by(Comment.created_at)
        .all()
    )