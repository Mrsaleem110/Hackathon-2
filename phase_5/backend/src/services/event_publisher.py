import asyncio
import json
from typing import Any, Dict
from dapr.ext.fastapi import DaprApp
from dapr.clients import DaprClient
from fastapi import FastAPI
from ..schemas.events import TaskEvent

class EventPublisherService:
    def __init__(self):
        self.dapr_client = DaprClient()
        self.pubsub_name = "pubsub"

    async def publish_task_event(self, event: TaskEvent) -> None:
        """
        Publish a task event to the event stream
        """
        try:
            # Serialize the event to JSON
            event_data = event.dict()
            event_json = json.dumps(event_data)

            # Publish to Dapr pubsub
            await self.dapr_client.publish_event_async(
                pubsub_name=self.pubsub_name,
                topic_name="task-events",
                data=event_json,
                data_content_type="application/json"
            )

            print(f"Published event: {event.event_type} for task {event.task_id}")

        except Exception as e:
            print(f"Error publishing event: {e}")
            # Log error for monitoring
            raise e

    async def publish_reminder_event(self, event: TaskEvent) -> None:
        """
        Publish a reminder event to the event stream
        """
        try:
            # Serialize the event to JSON
            event_data = event.dict()
            event_json = json.dumps(event_data)

            # Publish to Dapr pubsub
            await self.dapr_client.publish_event_async(
                pubsub_name=self.pubsub_name,
                topic_name="reminders",
                data=event_json,
                data_content_type="application/json"
            )

            print(f"Published reminder: {event.event_type} for task {event.task_id}")

        except Exception as e:
            print(f"Error publishing reminder event: {e}")
            raise e

    async def publish_task_updates(self, event: TaskEvent) -> None:
        """
        Publish a task update event to the event stream
        """
        try:
            # Serialize the event to JSON
            event_data = event.dict()
            event_json = json.dumps(event_data)

            # Publish to Dapr pubsub
            await self.dapr_client.publish_event_async(
                pubsub_name=self.pubsub_name,
                topic_name="task-updates",
                data=event_json,
                data_content_type="application/json"
            )

            print(f"Published update: {event.event_type} for task {event.task_id}")

        except Exception as e:
            print(f"Error publishing task update event: {e}")
            raise e

# Global instance
event_publisher_service = EventPublisherService()