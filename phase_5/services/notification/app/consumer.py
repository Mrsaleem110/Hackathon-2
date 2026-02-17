import asyncio
from datetime import datetime
from typing import Dict, Any
import json
import uuid
from dapr.ext.fastapi import DaprApp
from fastapi import FastAPI, HTTPException
from dapr.clients import DaprClient
from .notifiers import notification_service

app = FastAPI(title="Notification Service - Reminder Consumer")
dapr_app = DaprApp(app)
dapr_client = DaprClient()

@app.get("/")
async def root():
    return {"message": "Notification Service - Reminder Consumer"}

@dapr_app.subscribe(pubsub='pubsub', topic='reminders')
async def reminder_event_handler(event_data: Dict[str, Any]):
    """
    Handle incoming reminder events to send notifications
    """
    try:
        print(f"Received reminder event: {event_data}")

        # Extract reminder details
        task_id = event_data.get('task_id')
        user_id = event_data.get('user_id')
        task_title = event_data.get('task_title', 'Untitled Task')
        reminder_time = event_data.get('reminder_time')
        scheduled_at = event_data.get('scheduled_at')

        print(f"Processing reminder for task {task_id}, user {user_id}, time {reminder_time}")

        # Send notification
        results = await notification_service.process_reminder_payload(event_data)

        print(f"Reminder processed for task {task_id}, results: {results}")

        # Publish event that reminder was processed
        processed_payload = {
            "task_id": task_id,
            "user_id": user_id,
            "processed_at": datetime.utcnow().isoformat(),
            "results": results
        }

        await dapr_client.publish_event_async(
            pubsub_name="pubsub",
            topic_name="reminders-processed",
            data=json.dumps(processed_payload),
            data_content_type="application/json"
        )

    except Exception as e:
        print(f"Error processing reminder event: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.on_event('startup')
async def startup():
    print("Notification Service - Reminder Consumer starting up...")

@app.on_event('shutdown')
async def shutdown():
    print("Notification Service - Reminder Consumer shutting down...")
    dapr_client.close()