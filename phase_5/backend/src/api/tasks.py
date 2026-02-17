from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
import uuid
from datetime import datetime

from ..database.connection import get_session
from ..models.task import Task, TaskCreate, TaskUpdate, TaskCreateRequest
from ..services.task_service import TaskService
from ..auth import require_auth, User

# Task management routes
router = APIRouter(tags=["tasks"])

@router.get("/", response_model=List[Task])
async def get_tasks(
    current_user: User = Depends(require_auth()),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the authenticated user.
    """
    tasks = TaskService.get_tasks_by_user(session, current_user.id)
    return tasks

@router.post("/", response_model=Task)
async def create_task(
    task_request: TaskCreateRequest,
    current_user: User = Depends(require_auth()),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user.
    """
    # Check if this is a recurring task
    if task_request.recurrence_pattern:
        # Create a recurring task using the specialized method
        task_create = TaskCreate(
            title=task_request.title,
            description=task_request.description,
            user_id=current_user.id,
            priority=task_request.priority,
            due_date=task_request.due_date,
            reminder_time=task_request.reminder_time,
            recurrence_pattern=task_request.recurrence_pattern,
            tags=task_request.tags
        )
        created_task = await TaskService.create_recurring_task(session, task_create)
    else:
        # Create a regular task
        task_create = TaskCreate(
            title=task_request.title,
            description=task_request.description,
            completed=False,  # Default to False
            user_id=current_user.id,
            priority=task_request.priority,
            due_date=task_request.due_date,
            reminder_time=task_request.reminder_time,
            recurrence_pattern=task_request.recurrence_pattern,
            tags=task_request.tags
        )
        created_task = await TaskService.create_task(session, task_create)

    # Publish event for the new task
    from ..services.event_publisher import event_publisher_service
    from ..schemas.events import TaskCreatedEvent
    import datetime

    task_event = TaskCreatedEvent(
        event_type="created",
        task_id=created_task.id,
        user_id=created_task.user_id,
        timestamp=datetime.datetime.utcnow(),
        payload={
            "title": created_task.title,
            "description": created_task.description,
            "status": created_task.status,
            "priority": created_task.priority,
            "due_date": created_task.due_date,
            "tags": created_task.tags,
            "recurrence_info": {
                "has_recurrence": bool(created_task.recurrence_pattern),
                "series_id": str(created_task.series_id) if created_task.series_id else None
            }
        }
    )

    await event_publisher_service.publish_task_event(task_event)

    return created_task

@router.get("/{task_id}", response_model=Task)
async def get_task(
    task_id: str,
    current_user: User = Depends(require_auth()),
    session: Session = Depends(get_session)
):
    """
    Get a specific task by ID for the authenticated user.
    """
    try:
        task_uuid = uuid.UUID(task_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format"
        )

    task = TaskService.get_task_by_id(session, task_uuid)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only access your own tasks"
        )

    return task

@router.put("/{task_id}", response_model=Task)
async def update_task(
    task_id: str,
    task_update: TaskUpdate,
    current_user: User = Depends(require_auth()),
    session: Session = Depends(get_session)
):
    """
    Update a specific task by ID for the authenticated user.
    """
    try:
        task_uuid = uuid.UUID(task_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format"
        )

    task = TaskService.get_task_by_id(session, task_uuid)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only update your own tasks"
        )

    # Store original values to check for changes
    original_completed = task.completed
    original_series_id = task.series_id
    original_reminder_time = task.reminder_time

    updated_task = await TaskService.update_task(session, task_uuid, task_update)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # If the task was marked as completed and it's a recurring task, process it
    if updated_task.completed and not original_completed and updated_task.series_id:
        updated_task = await TaskService.process_completed_recurring_task(session, task_uuid)

        # Publish recurring task event
        from ..services.event_publisher import event_publisher_service
        from ..schemas.events import RecurringEvent
        import datetime

        recurring_event = RecurringEvent(
            event_type="task_completed_trigger",
            task_id=updated_task.id,
            user_id=updated_task.user_id,
            timestamp=datetime.datetime.utcnow(),
            payload={
                "action": "next_occurrence_processed",
                "series_id": str(updated_task.series_id) if updated_task.series_id else None,
                "original_task_id": str(task_uuid)
            }
        )

        await event_publisher_service.publish_recurring_task_event(recurring_event)

    # Publish update event
    from ..services.event_publisher import event_publisher_service
    from ..schemas.events import TaskUpdatedEvent
    import datetime

    task_event = TaskUpdatedEvent(
        event_type="updated",
        task_id=updated_task.id,
        user_id=updated_task.user_id,
        timestamp=datetime.datetime.utcnow(),
        payload={
            "title": updated_task.title,
            "description": updated_task.description,
            "status": updated_task.status,
            "priority": updated_task.priority,
            "completed": updated_task.completed,
            "due_date": updated_task.due_date,
            "tags": updated_task.tags,
            "reminder_time_changed": original_reminder_time != updated_task.reminder_time
        }
    )

    await event_publisher_service.publish_task_event(task_event)

    return updated_task

@router.delete("/{task_id}")
async def delete_task(
    task_id: str,
    current_user: User = Depends(require_auth()),
    session: Session = Depends(get_session)
):
    """
    Delete a specific task by ID for the authenticated user.
    """
    try:
        task_uuid = uuid.UUID(task_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format"
        )

    task = TaskService.get_task_by_id(session, task_uuid)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only delete your own tasks"
        )

    success = TaskService.delete_task(session, task_uuid)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return {"message": "Task deleted successfully"}

# Recurring task endpoints
@router.post("/{task_id}/recurring", response_model=Task)
async def create_recurring_task(
    task_id: str,
    task_update: TaskUpdate,
    current_user: User = Depends(require_auth()),
    session: Session = Depends(get_session)
):
    """
    Create or update a recurring task pattern.
    """
    try:
        task_uuid = uuid.UUID(task_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format"
        )

    task = TaskService.get_task_by_id(session, task_uuid)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only modify your own tasks"
        )

    # Update the task with recurrence pattern
    updated_task = TaskService.update_task(session, task_uuid, task_update)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return updated_task

@router.get("/recurring/{series_id}", response_model=List[Task])
async def get_recurring_task_occurrences(
    series_id: str,
    current_user: User = Depends(require_auth()),
    session: Session = Depends(get_session)
):
    """
    Get all occurrences of a recurring task series.
    """
    # This would require a more complex implementation to track task series
    # For now, this is a placeholder
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Recurring task series tracking not fully implemented yet"
    )