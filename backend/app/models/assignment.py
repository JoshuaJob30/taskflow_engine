#backend/app/models/assignment.py
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class TaskAssignment(Base):
    __tablename__ = "task_assignments"

    task_id = Column(
        Integer,
        ForeignKey("tasks.task_id"),
        primary_key=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False,
        index=True
    )

    assigned_at = Column(DateTime(timezone=True), server_default=func.now())

    task = relationship("Task", back_populates="assignment")
    user = relationship("User", back_populates="assignments")