from datetime import datetime, timedelta
from typing import Optional
import uuid
from dapr.clients import DaprClient
from dapr.ext.workflow import WorkflowRuntime
from ..models.task import Task
from sqlmodel import Session
import json

class ReminderService:
    def __init__(self):
        self.dapr_client = DaprClient()
        self.workflow_runtime = None  # This would be configured for Dapr workflows

    async def schedule_reminder(
        self,
        task_id: uuid.UUID,
        reminder_time: datetime,
        user_id: str,
        task_title: str
    ):
        """
        Schedule a reminder for a specific task at the specified time
        This is a placeholder implementation - in a real implementation,
        this would use Dapr Jobs API or similar scheduling mechanism
        """
        try:
            # In a real implementation, this would schedule a job via Dapr Jobs API
            # For now we'll just simulate by publishing a delayed message
            print(f"Scheduling reminder for task {task_id} at {reminder_time}")

            # Create a payload with reminder details
            reminder_payload = {
                "task_id": str(task_id),
                "user_id": user_id,
                "task_title": task_title,
                "reminder_time": reminder_time.isoformat(),
                "scheduled_at": datetime.utcnow().isoformat()
            }

            # In real implementation, we would use Dapr Jobs API to schedule this
            # For now, we'll publish to a dedicated reminders topic
            await self.dapr_client.publish_event_async(
                pubsub_name="pubsub",
                topic_name="reminders",
                data=json.dumps(reminder_payload),
                data_content_type="application/json"
            )

            print(f"Reminder scheduled for task {task_id} at {reminder_time}")
            return True

        except Exception as e:
            print(f"Error scheduling reminder: {e}")
            return False

    async def cancel_reminder(self, task_id: uuid.UUID):
        """
        Cancel a scheduled reminder for a task
        """
        try:
            print(f"Cancelling reminder for task {task_id}")
            # In real implementation, this would cancel the scheduled job via Dapr Jobs API
            return True
        except Exception as e:
            print(f"Error cancelling reminder: {e}")
            return False

    async def schedule_reminder_for_task(self, session: Session, task: Task):
        """
        Schedule a reminder for a task if it has reminder_time set
        """
        if not task.reminder_time:
            return False

        # Validate that reminder time is in the future
        if task.reminder_time <= datetime.utcnow():
            print(f"Reminder time {task.reminder_time} is in the past, not scheduling")
            return False

        return await self.schedule_reminder(
            task_id=task.id,
            reminder_time=task.reminder_time,
            user_id=task.user_id,
            task_title=task.title
        )

    async def handle_reminder_completion(self, task_id: uuid.UUID):
        """
        Handle the completion of a reminder (e.g., mark as sent)
        """
        try:
            print(f"Handling completion of reminder for task {task_id}")
            # In real implementation, this might update a reminder status
            return True
        except Exception as e:
            print(f"Error handling reminder completion: {e}")
            return False

reminder_service = ReminderService()