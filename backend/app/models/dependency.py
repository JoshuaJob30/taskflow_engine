#backend/app/models/dependency.py
from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base

class TaskDependency(Base):
    __tablename__ = "task_dependencies"

    dependency_id = Column(Integer, primary_key=True, index=True)

    task_id = Column(
        Integer,
        ForeignKey("tasks.task_id"),
        nullable=False,
        index=True
    )

    depends_on_task_id = Column(
        Integer,
        ForeignKey("tasks.task_id"),
        nullable=False,
        index=True
    )

    task = relationship(
        "Task",
        foreign_keys=[task_id],
        back_populates="dependencies"
    )

    depends_on_task = relationship(
        "Task",
        foreign_keys=[depends_on_task_id],
        back_populates="dependent_tasks"
    )

    __table_args__ = (
        UniqueConstraint(
            "task_id",
            "depends_on_task_id",
            name="uq_task_dependency"
        ),
    )