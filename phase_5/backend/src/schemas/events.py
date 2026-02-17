from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
import uuid

class TaskEvent(BaseModel):
    event_type: str  # "created", "updated", "completed", "deleted", "reminder", "recurring"
    task_id: uuid.UUID
    timestamp: datetime
    user_id: str
    payload: Optional[Dict[str, Any]] = None
    version: str = "1.0.0"

class TaskCreatedEvent(TaskEvent):
    event_type: str = "created"
    payload: Dict[str, Any]

class TaskUpdatedEvent(TaskEvent):
    event_type: str = "updated"
    payload: Dict[str, Any]

class TaskCompletedEvent(TaskEvent):
    event_type: str = "completed"
    payload: Dict[str, Any]

class TaskDeletedEvent(TaskEvent):
    event_type: str = "deleted"
    payload: Dict[str, Any]

class ReminderEvent(TaskEvent):
    event_type: str = "reminder"
    payload: Dict[str, Any]

class RecurringEvent(TaskEvent):
    event_type: str = "recurring"
    payload: Dict[str, Any]