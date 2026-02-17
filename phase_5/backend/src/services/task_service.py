from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
import uuid
from ..models.task import Task, TaskCreate, TaskUpdate, TaskSeries
from .recurrence_service import RecurrenceService
from .reminder_service import reminder_service

class TaskService:
    """Service class for handling task-related operations."""

    @staticmethod
    async def create_task(session: Session, task_create: TaskCreate) -> Task:
        """Create a new task."""
        # Create task instance with all fields
        task = Task(
            title=task_create.title,
            description=task_create.description,
            completed=task_create.completed or False,
            user_id=task_create.user_id,
            priority=task_create.priority,
            due_date=task_create.due_date,
            reminder_time=task_create.reminder_time,
            recurrence_pattern=task_create.recurrence_pattern,
            tags=task_create.tags or []
        )
        session.add(task)
        session.commit()
        session.refresh(task)

        # Schedule reminder if specified
        if task.reminder_time:
            await reminder_service.schedule_reminder_for_task(session, task)

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
    async def update_task(session: Session, task_id: uuid.UUID, task_update: TaskUpdate) -> Optional[Task]:
        """Update a task."""
        task = session.get(Task, task_id)
        if not task:
            return None

        # Check if reminder time is being updated
        old_reminder_time = task.reminder_time

        # Update only the fields that are provided
        update_data = task_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)

        # Handle reminder scheduling/cancellation based on changes
        if old_reminder_time != task.reminder_time:
            if old_reminder_time:
                # Cancel the old reminder
                await reminder_service.cancel_reminder(task_id)

            if task.reminder_time:
                # Schedule a new reminder
                await reminder_service.schedule_reminder_for_task(session, task)

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

    @staticmethod
    def create_task_from_data(session: Session, task: Task) -> Task:
        """Create a task from a Task model instance."""
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    async def create_recurring_task(session: Session, task_create: TaskCreate) -> Task:
        """Create a recurring task with series."""
        # Create a new TaskSeries first
        task_series = TaskSeries(
            title=task_create.title,
            description=task_create.description,
            user_id=task_create.user_id,
            recurrence_pattern=task_create.recurrence_pattern
        )
        session.add(task_series)
        session.commit()
        session.refresh(task_series)

        # Create the first occurrence of the recurring task
        task = Task(
            title=task_create.title,
            description=task_create.description,
            completed=task_create.completed or False,
            user_id=task_create.user_id,
            priority=task_create.priority,
            due_date=task_create.due_date,
            reminder_time=task_create.reminder_time,
            recurrence_pattern=task_create.recurrence_pattern,
            tags=task_create.tags or [],
            series_id=task_series.id  # Link to the series
        )
        session.add(task)
        session.commit()
        session.refresh(task)

        # Schedule reminder if specified
        if task.reminder_time:
            await reminder_service.schedule_reminder_for_task(session, task)

        return task

    @staticmethod
    async def process_completed_recurring_task(session: Session, task_id: uuid.UUID) -> Optional[Task]:
        """Process a completed recurring task and create the next occurrence if needed."""
        completed_task = session.get(Task, task_id)
        if not completed_task or not completed_task.series_id:
            return None

        # Update the completed task
        completed_task.completed = True
        completed_task.completed_at = datetime.utcnow()
        session.add(completed_task)

        # Cancel any existing reminder for this completed task
        await reminder_service.cancel_reminder(task_id)

        # Get the series to check recurrence pattern
        series = session.get(TaskSeries, completed_task.series_id)
        if not series or not series.recurrence_pattern:
            session.commit()
            return completed_task

        # Calculate next occurrence date
        next_occurrence_date = RecurrenceService.calculate_next_occurrence(
            completed_task.created_at,
            series.recurrence_pattern
        )

        new_task = None
        if next_occurrence_date:
            # Create the next occurrence
            new_task = RecurrenceService.create_next_occurrence(
                session,
                completed_task,
                next_occurrence_date
            )

            # Schedule reminder for the new task if it has a reminder time
            if new_task and new_task.reminder_time:
                await reminder_service.schedule_reminder_for_task(session, new_task)

        session.commit()
        if new_task:
            session.refresh(new_task)

        session.refresh(completed_task)
        return completed_task

    @staticmethod
    def get_task_series(session: Session, series_id: uuid.UUID) -> Optional[TaskSeries]:
        """Get a task series by its ID."""
        return session.get(TaskSeries, series_id)

    @staticmethod
    def get_tasks_by_series(session: Session, series_id: uuid.UUID) -> List[Task]:
        """Get all tasks in a series."""
        statement = select(Task).where(Task.series_id == series_id)
        return session.exec(statement).all()