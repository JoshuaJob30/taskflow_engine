# backend/app/routes/task_routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.task_schema import (
    TaskCreate,
    TaskResponse,
    TaskStatusUpdate,
    TaskAssignRequest,
    TaskDependencyCreate,
    TaskDependencyResponse,
    TaskHistoryResponse,
)
from app.schemas.comment_schema import CommentCreate, CommentResponse
from app.services import task_service, dependency_service

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)

@router.post("", response_model=TaskResponse)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
):
    return task_service.create_task(db, task_data)

@router.get("", response_model=list[TaskResponse])
def get_all_tasks(
    db: Session = Depends(get_db),
):
    return task_service.get_all_tasks(db)

@router.get("/{task_id}", response_model=TaskResponse)
def get_task_by_id(
    task_id: int,
    db: Session = Depends(get_db),
):
    return task_service.get_task_by_id(db, task_id)

@router.put("/{task_id}/assign")
def assign_task(
    task_id: int,
    assignment_data: TaskAssignRequest,
    db: Session = Depends(get_db),
):
    assignment = task_service.assign_task(
        db=db,
        task_id=task_id,
        user_id=assignment_data.user_id,
    )

    return {
        "message": "Task assigned successfully",
        "task_id": assignment.task_id,
        "user_id": assignment.user_id,
        "assigned_at": assignment.assigned_at,
    }

@router.put("/{task_id}/status", response_model=TaskResponse)
def update_task_status(
    task_id: int,
    status_update: TaskStatusUpdate,
    db: Session = Depends(get_db),
):
    return task_service.update_task_status(
        db=db,
        task_id=task_id,
        status_update=status_update,
    )

@router.post("/{task_id}/dependencies", response_model=TaskDependencyResponse)
def add_dependency(
    task_id: int,
    dependency_data: TaskDependencyCreate,
    db: Session = Depends(get_db),
):
    return dependency_service.add_dependency(
        db=db,
        task_id=task_id,
        depends_on_task_id=dependency_data.depends_on_task_id,
    )

@router.get("/{task_id}/dependencies", response_model=list[TaskDependencyResponse])
def get_dependencies_for_task(
    task_id: int,
    db: Session = Depends(get_db),
):
    return dependency_service.get_dependencies_for_task(db, task_id)

@router.post("/{task_id}/comments", response_model=CommentResponse)
def add_comment(
    task_id: int,
    comment_data: CommentCreate,
    db: Session = Depends(get_db),
):
    return task_service.add_comment(
        db=db,
        task_id=task_id,
        comment_data=comment_data,
    )

@router.get("/{task_id}/comments", response_model=list[CommentResponse])
def get_comments_for_task(
    task_id: int,
    db: Session = Depends(get_db),
):
    return task_service.get_comments_for_task(db, task_id)

@router.get("/{task_id}/history", response_model=list[TaskHistoryResponse])
def get_task_history(
    task_id: int,
    db: Session = Depends(get_db),
):
    return task_service.get_task_history(db, task_id)