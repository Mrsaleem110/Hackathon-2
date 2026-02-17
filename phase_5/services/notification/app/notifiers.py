from datetime import datetime
from typing import Dict, Any, List
import asyncio
import json
from dapr.clients import DaprClient
from .storage import notification_storage

class NotificationService:
    """
    Service to handle different notification channels
    """
    def __init__(self):
        self.dapr_client = DaprClient()
        self.channels = {
            'console': ConsoleNotifier(),
            'email': EmailNotifier(),
            'push': PushNotifier(),
        }

    async def send_notification(
        self,
        user_id: str,
        task_id: str,
        task_title: str,
        message: str,
        channels: List[str] = ['console']
    ):
        """
        Send notification through specified channels
        """
        results = {}

        for channel in channels:
            if channel in self.channels:
                try:
                    result = await self.channels[channel].send(user_id, task_id, task_title, message)
                    results[channel] = result
                except Exception as e:
                    results[channel] = {"status": "error", "error": str(e)}
            else:
                results[channel] = {"status": "error", "error": f"Channel {channel} not supported"}

        # Store the notification record for audit trail
        await asyncio.get_event_loop().run_in_executor(
            None,
            notification_storage.save_notification_record,
            task_id,
            user_id,
            task_title,
            message,
            results
        )

        return results

    async def process_reminder_payload(self, payload: Dict[str, Any]):
        """
        Process a reminder payload and send notifications
        """
        user_id = payload.get('user_id')
        task_id = payload.get('task_id')
        task_title = payload.get('task_title', 'Untitled')
        reminder_time = payload.get('reminder_time')

        message = f"Reminder: Task '{task_title}' is due soon!"

        # Send notification through default channels
        results = await self.send_notification(
            user_id=user_id,
            task_id=task_id,
            task_title=task_title,
            message=message,
            channels=['console']  # Default to console for testing
        )

        # Log the results
        for channel, result in results.items():
            print(f"Notification to {user_id} via {channel}: {result}")

        return results

    async def cleanup_job(self, job_id: str):
        """
        Clean up resources after job completion
        """
        print(f"Cleaning up resources for job {job_id}")
        # In real implementation, this would remove scheduled job records
        return True


class NotifierBase:
    async def send(self, user_id: str, task_id: str, task_title: str, message: str) -> Dict[str, Any]:
        raise NotImplementedError("Subclasses must implement send method")


class ConsoleNotifier(NotifierBase):
    async def send(self, user_id: str, task_id: str, task_title: str, message: str) -> Dict[str, Any]:
        """
        Send notification to console (for testing)
        """
        print(f"CONSOLE NOTIFICATION: {message}")
        print(f"  - User ID: {user_id}")
        print(f"  - Task ID: {task_id}")
        print(f"  - Task Title: {task_title}")
        print(f"  - Timestamp: {datetime.utcnow().isoformat()}")
        return {"status": "sent", "channel": "console", "timestamp": datetime.utcnow().isoformat()}


class EmailNotifier(NotifierBase):
    async def send(self, user_id: str, task_id: str, task_title: str, message: str) -> Dict[str, Any]:
        """
        Send notification via email
        """
        # In a real implementation, this would send an email
        print(f"EMAIL NOTIFICATION: {message} to user {user_id}")
        return {"status": "sent", "channel": "email", "timestamp": datetime.utcnow().isoformat()}


class PushNotifier(NotifierBase):
    async def send(self, user_id: str, task_id: str, task_title: str, message: str) -> Dict[str, Any]:
        """
        Send notification via push notification
        """
        # In a real implementation, this would send a push notification
        print(f"PUSH NOTIFICATION: {message} to user {user_id}")
        return {"status": "sent", "channel": "push", "timestamp": datetime.utcnow().isoformat()}


# Global instance
notification_service = NotificationService()