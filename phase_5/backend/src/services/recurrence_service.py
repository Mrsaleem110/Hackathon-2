from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from enum import Enum
from ..models.task import Task, TaskSeries
from sqlmodel import Session
import uuid
from datetime import datetime, timedelta
import json

class RecurrenceType(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"

class RecurrenceService:
    @staticmethod
    def calculate_next_occurrence(
        current_date: datetime,
        recurrence_pattern: Dict[str, Any]
    ) -> Optional[datetime]:
        """
        Calculate the next occurrence based on the recurrence pattern
        """
        recurrence_type = recurrence_pattern.get('type', 'daily')
        interval = recurrence_pattern.get('interval', 1)
        end_date = recurrence_pattern.get('end_date')
        count = recurrence_pattern.get('count')

        # Check if recurrence should end
        if end_date and current_date.date() >= end_date.date():
            return None
        if count and recurrence_pattern.get('occurrence_count', 0) >= count:
            return None

        # Calculate next occurrence based on recurrence type
        if recurrence_type == 'daily':
            next_date = current_date + timedelta(days=interval)
        elif recurrence_type == 'weekly':
            # Ensure we maintain the same day of the week
            next_date = current_date + timedelta(weeks=interval)
        elif recurrence_type == 'monthly':
            # Handle month boundaries carefully
            next_date = RecurrenceService._add_months(current_date, interval)
        elif recurrence_type == 'yearly':
            next_date = current_date.replace(year=current_date.year + interval)
        else:
            # Unknown recurrence type, return None
            return None

        # Check against end date again after calculation
        if end_date and next_date.date() > end_date.date():
            return None

        return next_date

    @staticmethod
    def _add_months(date: datetime, months: int) -> datetime:
        """
        Add months to a date, handling month boundaries properly
        """
        month = date.month - 1 + months
        year = date.year + month // 12
        month = month % 12 + 1
        day = min(date.day, RecurrenceService._days_in_month(year, month))

        # Return a new datetime with the same time components
        return date.replace(year=year, month=month, day=day)

    @staticmethod
    def _days_in_month(year: int, month: int) -> int:
        """
        Get the number of days in a month
        """
        import calendar
        return calendar.monthrange(year, month)[1]

    @staticmethod
    def create_next_occurrence(
        session: Session,
        original_task: Task,
        next_occurrence_date: datetime
    ) -> Optional[Task]:
        """
        Create a new task occurrence based on the original task
        """
        # Create a new task with the same properties as the original
        new_task_data = {
            'title': original_task.title,
            'description': original_task.description,
            'user_id': original_task.user_id,
            'status': 'active',
            'priority': original_task.priority,
            'due_date': original_task.due_date,
            'reminder_time': original_task.reminder_time,
            'recurrence_pattern': original_task.recurrence_pattern,
            # Link to the series
            'series_id': original_task.series_id
        }

        # Calculate due date and reminder time based on the recurrence
        if original_task.due_date:
            # Calculate new due date based on the recurrence pattern
            original_task_date = original_task.created_at
            new_task_date = next_occurrence_date
            date_diff = new_task_date - original_task_date
            new_due_date = original_task.due_date + date_diff
            new_task_data['due_date'] = new_due_date

        if original_task.reminder_time:
            # Calculate new reminder time based on the recurrence pattern
            original_task_date = original_task.created_at
            new_task_date = next_occurrence_date
            date_diff = new_task_date - original_task_date
            new_reminder_time = original_task.reminder_time + date_diff
            new_task_data['reminder_time'] = new_reminder_time

        # Create new task instance
        new_task = Task(
            title=new_task_data['title'],
            description=new_task_data['description'],
            user_id=new_task_data['user_id'],
            status=new_task_data['status'],
            priority=new_task_data['priority'],
            due_date=new_task_data['due_date'],
            reminder_time=new_task_data['reminder_time'],
            recurrence_pattern=new_task_data['recurrence_pattern'],
            series_id=new_task_data['series_id'],
        )

        # Add to session and commit
        session.add(new_task)
        session.commit()
        session.refresh(new_task)

        return new_task

    @staticmethod
    def get_series_tasks(
        session: Session,
        series_id: uuid.UUID
    ) -> list:
        """
        Get all tasks in a recurrence series
        """
        from sqlmodel import select
        statement = select(Task).where(Task.series_id == series_id)
        results = session.exec(statement).all()
        return results