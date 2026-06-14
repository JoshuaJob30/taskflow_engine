# backend/app/repositories/report_repo.py
from sqlalchemy import case, func
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.project import Project
from app.models.task import Task
from app.models.assignment import TaskAssignment
from app.models.dependency import TaskDependency
from app.utils.constants import ACTIVE_STATUSES

def get_user_workload_report(db: Session):
    return (
        db.query(
            User.user_id.label("user_id"),
            User.name.label("user_name"),
            func.count(Task.task_id).label("active_task_count"),
        )
        .outerjoin(TaskAssignment, User.user_id == TaskAssignment.user_id)
        .outerjoin(Task, TaskAssignment.task_id == Task.task_id)
        .filter((Task.status.in_(ACTIVE_STATUSES)) | (Task.task_id.is_(None)))
        .group_by(User.user_id, User.name)
        .order_by(User.user_id)
        .all()
    )

def get_project_progress_report(db: Session):
    closed_case = case(
        (Task.status == "CLOSED", 1),
        else_=0,
    )

    return (
        db.query(
            Project.project_id.label("project_id"),
            Project.name.label("project_name"),
            func.count(Task.task_id).label("total_tasks"),
            func.sum(closed_case).label("closed_tasks"),
        )
        .outerjoin(Task, Project.project_id == Task.project_id)
        .group_by(Project.project_id, Project.name)
        .order_by(Project.project_id)
        .all()
    )

def get_blocked_tasks_report(db: Session):
    blocking_task = Task.__table__.alias("blocking_task")

    return (
        db.query(
            Task.task_id.label("task_id"),
            Task.title.label("title"),
            Task.status.label("status"),
            TaskDependency.depends_on_task_id.label("blocking_task_id"),
            blocking_task.c.status.label("blocking_task_status"),
        )
        .join(TaskDependency, Task.task_id == TaskDependency.task_id)
        .join(
            blocking_task,
            TaskDependency.depends_on_task_id == blocking_task.c.task_id,
        )
        .filter(blocking_task.c.status != "RESOLVED")
        .order_by(Task.task_id)
        .all()
    )