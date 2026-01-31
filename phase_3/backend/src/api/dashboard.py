from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session, select
import logging
from typing import List

logger = logging.getLogger(__name__)

from ..database.connection import get_session
from ..models.task import Task
from ..models.user import User
from ..auth import require_auth, User as AuthUser

router = APIRouter(tags=["dashboard"])



@router.get("/stats")
async def get_dashboard_stats(
    current_user: AuthUser = Depends(require_auth()),
    session: Session = Depends(get_session)
):
    """Get dashboard statistics"""
    try:
        user_id = current_user.id

        # Get all tasks for the current user
        statement = select(Task).where(Task.user_id == user_id)
        tasks = session.exec(statement).all()

        # Calculate task statistics
        total_tasks = len(tasks)
        completed_tasks = len([task for task in tasks if task.completed])
        pending_tasks = total_tasks - completed_tasks

        # For now, return static chat count (would need a Chat model to make dynamic)
        total_chats = 0

        # Get recent activity (most recent 5 tasks)
        recent_tasks = sorted(tasks, key=lambda x: x.created_at, reverse=True)[:5]
        recent_activity = [
            {
                "id": str(task.id),
                "title": task.title,
                "completed": task.completed,
                "created_at": task.created_at.isoformat() if task.created_at else None
            }
            for task in recent_tasks
        ]

        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "total_chats": total_chats,
            "recent_activity": recent_activity
        }
    except Exception as e:
        logger.error(f"Error fetching dashboard stats: {str(e)}")
        # Still return safe defaults on error
        return {
            "total_tasks": 0,
            "completed_tasks": 0,
            "pending_tasks": 0,
            "total_chats": 0,
            "recent_activity": []
        }


@router.get("/overview")
async def get_dashboard_overview(
    current_user: AuthUser = Depends(require_auth()),
    session: Session = Depends(get_session)
):
    """Get dashboard overview"""
    try:
        user_id = current_user.id

        # Get all tasks for the current user
        statement = select(Task).where(Task.user_id == user_id)
        tasks = session.exec(statement).all()

        # Calculate task statistics
        tasks_count = len(tasks)
        completed_count = len([task for task in tasks if task.completed])
        pending_count = tasks_count - completed_count

        # Get recent tasks (most recent 5)
        recent_tasks = sorted(tasks, key=lambda x: x.created_at, reverse=True)[:5]

        # Prepare chart data (for example, tasks by completion status)
        chart_data = [
            {"status": "completed", "count": completed_count},
            {"status": "pending", "count": pending_count}
        ]

        return {
            "user": {
                "id": current_user.id,
                "email": current_user.email,
                "name": current_user.name
            },
            "stats": {
                "tasks_count": tasks_count,
                "completed_count": completed_count,
                "pending_count": pending_count
            },
            "recent_tasks": [
                {
                    "id": str(task.id),
                    "title": task.title,
                    "completed": task.completed,
                    "priority": task.priority,
                    "due_date": task.due_date,
                    "created_at": task.created_at.isoformat() if task.created_at else None
                }
                for task in recent_tasks
            ],
            "chart_data": chart_data
        }
    except Exception as e:
        logger.error(f"Error fetching dashboard overview: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch dashboard: {str(e)}")
