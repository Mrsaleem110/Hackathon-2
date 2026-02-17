from datetime import datetime
from typing import Optional
from sqlmodel import Session
import uuid
from backend.src.models.task import Task
from backend.src.services.recurrence_service import RecurrenceService

class RecurrenceProcessor:
    """
    A processor class specifically for handling recurrence pattern operations
    """

    @staticmethod
    def create_next_task_occurrence(
        session: Session,
        original_task: Task,
        next_occurrence_date: datetime
    ) -> Optional[Task]:
        """
        Create the next occurrence of a recurring task based on the original task
        and the calculated next occurrence date.
        """
        return RecurrenceService.create_next_occurrence(
            session,
            original_task,
            next_occurrence_date
        )

    @staticmethod
    def calculate_next_occurrence_date(
        current_date: datetime,
        recurrence_pattern: dict
    ) -> Optional[datetime]:
        """
        Calculate the next occurrence date based on the current date and recurrence pattern
        """
        return RecurrenceService.calculate_next_occurrence(
            current_date,
            recurrence_pattern
        )

    @staticmethod
    def validate_recurrence_pattern(recurrence_pattern: dict) -> bool:
        """
        Validate that the recurrence pattern has required fields and valid values
        """
        if not isinstance(recurrence_pattern, dict):
            return False

        required_fields = ['type']
        for field in required_fields:
            if field not in recurrence_pattern:
                return False

        recurrence_type = recurrence_pattern.get('type')
        valid_types = ['daily', 'weekly', 'monthly', 'yearly']

        if recurrence_type not in valid_types:
            return False

        # Validate interval if provided
        interval = recurrence_pattern.get('interval', 1)
        if not isinstance(interval, int) or interval < 1:
            return False

        # Validate count if provided
        count = recurrence_pattern.get('count')
        if count is not None and (not isinstance(count, int) or count < 1):
            return False

        return True