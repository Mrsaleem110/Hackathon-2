import asyncio
from datetime import datetime
from typing import Dict, Any
import json
import uuid
from dapr.ext.fastapi import DaprApp
from fastapi import FastAPI, HTTPException
from dapr.clients import DaprClient
from backend.src.services.recurrence_service import RecurrenceService
from backend.src.models.task import Task, TaskSeries
from backend.src.schemas.events import TaskEvent, RecurringEvent
from backend.src.database.connection import get_session
from sqlmodel import Session, select

app = FastAPI(title="Recurring Task Service")
dapr_app = DaprApp(app)
dapr_client = DaprClient()

@app.get("/")
async def root():
    return {"message": "Recurring Task Service"}

@dapr_app.subscribe(pubsub='pubsub', topic='task-events')
async def recurring_task_event_handler(event_data: Dict[str, Any]):
    """
    Handle incoming task events to process recurring tasks when completed
    """
    try:
        print(f"Received task event: {event_data}")

        # Extract event details
        event_type = event_data.get('event_type')
        task_id_str = event_data.get('task_id')
        user_id = event_data.get('user_id')
        payload = event_data.get('payload', {})

        # Convert task_id to UUID
        try:
            task_id = uuid.UUID(task_id_str)
        except ValueError:
            print(f"Invalid task ID format: {task_id_str}")
            return

        print(f"Processing {event_type} event for task {task_id} by user {user_id}")

        # Only process completed events for recurring tasks
        if event_type == 'completed':
            # Check if this is a recurring task by looking up the task
            await process_completed_recurring_task(task_id, user_id, payload)

    except Exception as e:
        print(f"Error processing task event: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def process_completed_recurring_task(task_id: uuid.UUID, user_id: str, payload: Dict[str, Any]):
    """
    Process a completed recurring task and create the next occurrence if needed.
    """
    print(f"Processing completed recurring task: {task_id}")

    # Create a database session
    session = next(get_session())

    try:
        # Get the completed task
        completed_task = session.get(Task, task_id)
        if not completed_task:
            print(f"Task not found: {task_id}")
            return

        # Check if this is a recurring task (has recurrence_pattern and series_id)
        if not completed_task.recurrence_pattern or not completed_task.series_id:
            print(f"Task {task_id} is not a recurring task")
            return

        print(f"Task {task_id} is recurring, processing next occurrence...")

        # Get the task series to check recurrence pattern
        series = session.get(TaskSeries, completed_task.series_id)
        if not series or not series.recurrence_pattern:
            print(f"Series not found or has no recurrence pattern: {completed_task.series_id}")
            return

        # Calculate next occurrence date
        next_occurrence_date = RecurrenceService.calculate_next_occurrence(
            completed_task.created_at,
            series.recurrence_pattern
        )

        # Create next occurrence if needed
        if next_occurrence_date:
            print(f"Creating next occurrence for task {task_id} at {next_occurrence_date}")

            # Use the RecurrenceService to create the next occurrence
            new_task = RecurrenceService.create_next_occurrence(
                session,
                completed_task,
                next_occurrence_date
            )

            if new_task:
                print(f"Created new task occurrence: {new_task.id}")

                # Publish event for the new task
                from backend.src.services.event_publisher import event_publisher_service
                from backend.src.schemas.events import TaskCreatedEvent

                new_task_event = TaskCreatedEvent(
                    event_type="created",
                    task_id=new_task.id,
                    user_id=new_task.user_id,
                    timestamp=datetime.utcnow(),
                    payload={
                        "title": new_task.title,
                        "description": new_task.description,
                        "due_date": new_task.due_date,
                        "recurrence_info": {
                            "is_occurrence": True,
                            "original_series_id": str(completed_task.series_id)
                        }
                    }
                )

                # Publish the event
                await event_publisher_service.publish_task_event(new_task_event)
        else:
            print(f"Recurrence pattern ended for series {completed_task.series_id}")

    except Exception as e:
        print(f"Error processing completed recurring task: {e}")
        raise
    finally:
        session.close()

@app.on_event('startup')
async def startup():
    print("Recurring Task Service starting up...")

@app.on_event('shutdown')
async def shutdown():
    print("Recurring Task Service shutting down...")
    dapr_client.close()