from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.base import Base
from app.db.session import engine
from app.models import (
    User,
    Project,
    Task,
    TaskAssignment,
    TaskDependency,
    TaskHistory,
    Comment,
)
from app.routes import (
    user_routes,
    project_routes,
    task_routes,
    report_routes,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Taskflow Engine API",
    description="Enterprise Task and Workflow Management Backend",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_routes.router)
app.include_router(project_routes.router)
app.include_router(task_routes.router)
app.include_router(report_routes.router)


@app.get("/")
def health_check():
    return {
        "status": "running",
        "service": "Taskflow Engine API",
    }