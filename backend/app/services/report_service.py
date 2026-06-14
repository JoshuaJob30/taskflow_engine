# backend/app/services/report_service.py
from sqlalchemy.orm import Session

from app.repositories import report_repo
from app.schemas.report_schema import (
    UserWorkloadReport,
    ProjectProgressReport,
    BlockedTaskReport,
)

def get_user_workload_report(db: Session) -> list:
    rows = report_repo.get_user_workload_report(db)

    return [
        UserWorkloadReport(
            user_id=row.user_id,
            user_name=row.user_name,
            active_task_count=row.active_task_count or 0,
        )
        for row in rows
    ]

def get_project_progress_report(db: Session) -> list:
    rows = report_repo.get_project_progress_report(db)

    report = []

    for row in rows:
        total_tasks = row.total_tasks or 0
        closed_tasks = row.closed_tasks or 0

        if total_tasks == 0:
            completion_percentage = 0.0
        else:
            completion_percentage = round((closed_tasks * 100) / total_tasks, 2)

        report.append(
            ProjectProgressReport(
                project_id=row.project_id,
                project_name=row.project_name,
                total_tasks=total_tasks,
                closed_tasks=closed_tasks,
                completion_percentage=completion_percentage,
            )
        )

    return report

def get_blocked_tasks_report(db: Session) -> list:
    rows = report_repo.get_blocked_tasks_report(db)

    return [
        BlockedTaskReport(
            task_id=row.task_id,
            title=row.title,
            status=row.status,
            blocking_task_id=row.blocking_task_id,
            blocking_task_status=row.blocking_task_status,
        )
        for row in rows
    ]