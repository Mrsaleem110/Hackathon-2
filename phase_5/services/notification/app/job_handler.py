from fastapi import FastAPI, HTTPException
from dapr.ext.workflow import DaprWorkflowRuntime
from dapr.clients import DaprClient
from datetime import datetime
import json
import asyncio
from typing import Dict, Any

app = FastAPI(title="Notification Service - Job Handler")

# Initialize Dapr clients
dapr_client = DaprClient()

class ReminderWorkflow:
    """
    A Dapr workflow to handle task reminders
    """
    async def run(self, ctx, input_data: Dict[str, Any]):
        """
        Execute the reminder workflow
        """
        try:
            print(f"Executing reminder workflow for task: {input_data.get('task_id')}")

            # Extract reminder data
            task_id = input_data.get('task_id')
            user_id = input_data.get('user_id')
            task_title = input_data.get('task_title')
            reminder_time = input_data.get('reminder_time')

            # Simulate reminder processing
            print(f"Processing reminder for task {task_id} at {reminder_time}")

            # In a real implementation, this would send the actual notification
            # For now, we'll just log it
            await self.send_notification(user_id, task_id, task_title)

            # Publish reminder sent event
            reminder_payload = {
                "task_id": task_id,
                "user_id": user_id,
                "task_title": task_title,
                "reminder_time": reminder_time,
                "sent_at": datetime.utcnow().isoformat()
            }

            await dapr_client.publish_event_async(
                pubsub_name="pubsub",
                topic_name="reminders-sent",
                data=json.dumps(reminder_payload),
                data_content_type="application/json"
            )

            print(f"Reminder sent for task {task_id}")
            return {"status": "success", "task_id": task_id}

        except Exception as e:
            print(f"Error in reminder workflow: {e}")
            return {"status": "error", "error": str(e)}

    async def send_notification(self, user_id: str, task_id: str, task_title: str):
        """
        Send the actual notification to the user
        """
        print(f"Sending notification to user {user_id} for task '{task_title}' (ID: {task_id})")
        # In real implementation, this would send email, push notification, etc.
        # For now, just logging as console output

# Initialize workflow runtime
workflow_runtime = DaprWorkflowRuntime()

@app.on_event('startup')
async def startup():
    # Register the workflow
    workflow_runtime.register_workflow(ReminderWorkflow)
    workflow_runtime.start()

@app.on_event('shutdown')
async def shutdown():
    dapr_client.close()
    if workflow_runtime:
        await workflow_runtime.shutdown()

@app.post("/api/jobs/schedule")
async def schedule_reminder_job(reminder_data: Dict[str, Any]):
    """
    Schedule a reminder job via Dapr workflow
    """
    try:
        print(f"Scheduling reminder job: {reminder_data}")

        # Start the reminder workflow
        workflow_id = f"reminder-{reminder_data['task_id']}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"

        # In a real implementation, we would schedule this to run at the specific reminder time
        # For now, we'll just run it immediately to simulate
        await dapr_client.start_workflow_by_id(
            workflow_component="dapr",
            workflow_name="reminder_workflow",
            instance_id=workflow_id,
            input_data=reminder_data
        )

        return {
            "workflow_id": workflow_id,
            "status": "scheduled",
            "task_id": reminder_data['task_id']
        }
    except Exception as e:
        print(f"Error scheduling reminder job: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/jobs/trigger")
async def trigger_reminder_job(payload: Dict[str, Any]):
    """
    Trigger endpoint for incoming job callbacks
    """
    print(f"Triggering reminder job with payload: {payload}")

    # Process the reminder
    task_id = payload.get('task_id')
    user_id = payload.get('user_id')
    task_title = payload.get('task_title')

    # For now, just log that reminder was triggered
    print(f"Reminder triggered for task {task_id}, user {user_id}, title '{task_title}'")

    return {
        "status": "processed",
        "task_id": task_id
    }

@app.get("/")
async def root():
    return {"message": "Notification Service with Job Handler Running"}