from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
import uuid
from ..models.task import Task, TaskCreate, TaskUpdate

class TaskService:
    """Service class for handling task-related operations."""

    @staticmethod
    def create_task(session: Session, task_create: TaskCreate) -> Task:
        """Create a new task."""
        task = Task.from_orm(task_create) if hasattr(Task, 'from_orm') else Task(
            title=task_create.title,
            description=task_create.description,
            completed=task_create.completed,
            user_id=task_create.user_id
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def get_task_by_id(session: Session, task_id: uuid.UUID) -> Optional[Task]:
        """Get a task by its ID."""
        return session.get(Task, task_id)

    @staticmethod
    def get_tasks_by_user(session: Session, user_id: str) -> List[Task]:
        """Get all tasks for a specific user."""
        statement = select(Task).where(Task.user_id == user_id)
        return session.exec(statement).all()

    @staticmethod
    def update_task(session: Session, task_id: uuid.UUID, task_update: TaskUpdate) -> Optional[Task]:
        """Update a task."""
        task = session.get(Task, task_id)
        if not task:
            return None

        # Update only the fields that are provided
        update_data = task_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def delete_task(session: Session, task_id: uuid.UUID) -> bool:
        """Delete a task."""
        task = session.get(Task, task_id)
        if not task:
            return False

        session.delete(task)
        session.commit()
        return True

    @staticmethod
    def complete_task(session: Session, task_id: uuid.UUID) -> Optional[Task]:
        """Mark a task as completed."""
        task = session.get(Task, task_id)
        if not task:
            return None

        task.completed = True
        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)
        return task