# backend/app/routes/report_routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.report_schema import (
    UserWorkloadReport,
    ProjectProgressReport,
    BlockedTaskReport,
)
from app.services import report_service

router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)

@router.get("/workload", response_model=list[UserWorkloadReport])
def get_user_workload_report(
    db: Session = Depends(get_db),
):
    return report_service.get_user_workload_report(db)

@router.get("/project-progress", response_model=list[ProjectProgressReport])
def get_project_progress_report(
    db: Session = Depends(get_db),
):
    return report_service.get_project_progress_report(db)

@router.get("/blocked-tasks", response_model=list[BlockedTaskReport])
def get_blocked_tasks_report(
    db: Session = Depends(get_db),
):
    return report_service.get_blocked_tasks_report(db)