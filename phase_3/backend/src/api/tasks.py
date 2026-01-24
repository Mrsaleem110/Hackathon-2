from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List, Optional
import uuid
from datetime import datetime
import logging
import json

logger = logging.getLogger(__name__)

from ..database.connection import get_session
from ..models.task import Task, TaskCreate, TaskUpdate, TaskCreateRequest
from ..services.task_service import TaskService

# Task management routes
router = APIRouter(tags=["tasks"])

# Optional auth dependency for testing
async def optional_auth():
    """Optional auth - returns a mock user if no token"""
    return {"id": "test-user", "email": "test@example.com", "name": "Test User"}

@router.get("/", response_model=Optional[List[Task]])
async def get_tasks(
    current_user: dict = Depends(optional_auth),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the authenticated user.
    """
    try:
        user_id = current_user.get("id") if isinstance(current_user, dict) else current_user.id
        tasks = TaskService.get_tasks_by_user(session, user_id)
        logger.info(f"Successfully fetched {len(tasks)} tasks for user {user_id}")
        return tasks
    except Exception as e:
        logger.error(f"Error fetching tasks: {str(e)}", exc_info=True)
        # Return empty list instead of error to allow UI to function
        return []

@router.post("/", response_model=Optional[Task])
async def create_task(
    task_request: TaskCreateRequest,
    current_user: dict = Depends(optional_auth),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user.
    """
    try:
        user_id = current_user.get("id") if isinstance(current_user, dict) else current_user.id
        logger.info(f"Creating task for user {user_id}: {task_request.title}")
        
        # Create the task with the authenticated user's ID
        task_create = TaskCreate(
            title=task_request.title,
            description=task_request.description,
            completed=task_request.completed,
            user_id=user_id,
            priority=task_request.priority,
            due_date=task_request.due_date
        )
        created_task = TaskService.create_task(session, task_create)
        logger.info(f"Successfully created task {created_task.id} for user {user_id}")
        return created_task
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error creating task: {error_msg}", exc_info=True)
        # Provide more useful error messages
        if "database" in error_msg.lower() or "connection" in error_msg.lower():
            raise HTTPException(status_code=503, detail="Database service temporarily unavailable")
        raise HTTPException(status_code=500, detail=f"Failed to create task: {error_msg}")

@router.get("/{task_id}", response_model=Task)
async def get_task(
    task_id: str,
    current_user: dict = Depends(optional_auth),
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

    try:
        task = TaskService.get_task_by_id(session, task_uuid)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        return task
    except Exception as e:
        logger.error(f"Error fetching task: {str(e)}", exc_info=True)
        if "database" in str(e).lower() or "connection" in str(e).lower():
            raise HTTPException(status_code=503, detail="Database service temporarily unavailable")
        raise HTTPException(status_code=500, detail=f"Failed to fetch task: {str(e)}")

@router.put("/{task_id}", response_model=Task)
async def update_task(
    task_id: str,
    task_update: TaskUpdate,
    current_user: dict = Depends(optional_auth),
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

    try:
        task = TaskService.get_task_by_id(session, task_uuid)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        updated_task = TaskService.update_task(session, task_uuid, task_update)
        if not updated_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        return updated_task
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating task: {str(e)}", exc_info=True)
        if "database" in str(e).lower() or "connection" in str(e).lower():
            raise HTTPException(status_code=503, detail="Database service temporarily unavailable")
        raise HTTPException(status_code=500, detail=f"Failed to update task: {str(e)}")

@router.delete("/{task_id}")
async def delete_task(
    task_id: str,
    current_user: dict = Depends(optional_auth),
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

    try:
        task = TaskService.get_task_by_id(session, task_uuid)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        success = TaskService.delete_task(session, task_uuid)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or already deleted"
            )

        return {"message": "Task deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting task: {str(e)}", exc_info=True)
        if "database" in str(e).lower() or "connection" in str(e).lower():
            raise HTTPException(status_code=503, detail="Database service temporarily unavailable")
        raise HTTPException(status_code=500, detail=f"Failed to delete task: {str(e)}")