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
    # Create the task with the authenticated user's ID
    task_create = TaskCreate(
        title=task_request.title,
        description=task_request.description,
        completed=task_request.completed,
        user_id=current_user.id,  # Use authenticated user ID from auth
        priority=task_request.priority,
        due_date=task_request.due_date
    )
    created_task = TaskService.create_task(session, task_create)
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

    updated_task = TaskService.update_task(session, task_uuid, task_update)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

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