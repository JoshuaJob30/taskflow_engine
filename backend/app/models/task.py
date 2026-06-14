#backend/app/models/task.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class Task(Base):
    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True, index=True)

    project_id = Column(Integer, ForeignKey("projects.project_id"), nullable=False)

    title = Column(String(200), nullable=False)
    description = Column(String(1000), nullable=True)

    status = Column(String(30), nullable=False, default="CREATED")
    priority = Column(String(20), nullable=False, default="MEDIUM")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=True)

    project = relationship("Project", back_populates="tasks")

    assignment = relationship(
        "TaskAssignment",
        back_populates="task",
        uselist=False,
        cascade="all, delete-orphan"
    )

    dependencies = relationship(
        "TaskDependency",
        foreign_keys="TaskDependency.task_id",
        back_populates="task",
        cascade="all, delete-orphan"
    )

    dependent_tasks = relationship(
        "TaskDependency",
        foreign_keys="TaskDependency.depends_on_task_id",
        back_populates="depends_on_task"
    )

    history_entries = relationship(
        "TaskHistory",
        back_populates="task",
        cascade="all, delete-orphan"
    )

    comments = relationship(
        "Comment",
        back_populates="task",
        cascade="all, delete-orphan"
    )