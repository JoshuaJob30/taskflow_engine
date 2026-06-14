from app.schemas.user_schema import UserCreate, UserResponse
from app.schemas.project_schema import ProjectCreate, ProjectResponse
from app.schemas.task_schema import (
    TaskCreate,
    TaskResponse,
    TaskStatusUpdate,
    TaskAssignRequest,
    TaskDependencyCreate,
    TaskHistoryResponse,
    TaskDependencyResponse,
)
from app.schemas.comment_schema import CommentCreate, CommentResponse
from app.schemas.report_schema import (
    UserWorkloadReport,
    ProjectProgressReport,
    BlockedTaskReport,
)