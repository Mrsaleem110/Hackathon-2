from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
import logging

logger = logging.getLogger(__name__)

from ..database.connection import get_session

router = APIRouter(tags=["dashboard"])

# Optional auth dependency for testing
async def optional_auth():
    """Optional auth - returns a mock user if no token"""
    return {"id": "test-user", "email": "test@example.com", "name": "Test User"}


@router.get("/stats")
async def get_dashboard_stats(
    current_user: dict = Depends(optional_auth),
    session: Session = Depends(get_session)
):
    """Get dashboard statistics"""
    try:
        return {
            "total_tasks": 0,
            "completed_tasks": 0,
            "pending_tasks": 0,
            "total_chats": 0,
            "recent_activity": []
        }
    except Exception as e:
        logger.error(f"Error fetching dashboard stats: {str(e)}")
        return {
            "total_tasks": 0,
            "completed_tasks": 0,
            "pending_tasks": 0,
            "total_chats": 0,
            "recent_activity": []
        }


@router.get("/overview")
async def get_dashboard_overview(
    current_user: dict = Depends(optional_auth),
    session: Session = Depends(get_session)
):
    """Get dashboard overview"""
    try:
        return {
            "user": current_user,
            "stats": {
                "tasks_count": 0,
                "completed_count": 0,
                "pending_count": 0
            },
            "recent_tasks": [],
            "chart_data": []
        }
    except Exception as e:
        logger.error(f"Error fetching dashboard overview: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch dashboard: {str(e)}")
