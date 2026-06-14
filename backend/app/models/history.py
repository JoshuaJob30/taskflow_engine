#backend/app/models/history.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class TaskHistory(Base):
    __tablename__ = "task_history"

    history_id = Column(Integer, primary_key=True, index=True)

    task_id = Column(
        Integer,
        ForeignKey("tasks.task_id"),
        nullable=False,
        index=True
    )

    old_status = Column(String(30), nullable=True)
    new_status = Column(String(30), nullable=False)

    change_reason = Column(String(500), nullable=True)

    changed_at = Column(DateTime(timezone=True), server_default=func.now())

    task = relationship("Task", back_populates="history_entries")
