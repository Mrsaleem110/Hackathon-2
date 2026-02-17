from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import List, Optional
from datetime import datetime
from ..database.connection import get_session
from ..models.task import Task
from ..auth import require_auth, User
from ..services.search_service import TaskSearchService, PriorityEnum

# Search and filter routes
router = APIRouter(tags=["task-search"])

@router.get("/search", response_model=dict)
async def search_tasks(
    query: Optional[str] = Query(None, description="Text to search in title and description"),
    status: Optional[str] = Query(None, description="Filter by status (active, completed, etc.)"),
    priority: Optional[PriorityEnum] = Query(None, description="Filter by priority (high, medium, low)"),
    tags: Optional[List[str]] = Query(None, description="Filter by tags"),
    due_date_from: Optional[datetime] = Query(None, description="Filter tasks with due date after this date"),
    due_date_to: Optional[datetime] = Query(None, description="Filter tasks with due date before this date"),
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    sort_by: str = Query("created_at", description="Sort by field (created_at, due_date, priority)"),
    sort_order: str = Query("desc", description="Sort order (asc, desc)"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    limit: int = Query(100, ge=1, le=1000, description="Pagination limit"),
    current_user: User = Depends(require_auth()),
    session: Session = Depends(get_session)
):
    """
    Search and filter tasks with various criteria
    """
    try:
        search_results = TaskSearchService.search_tasks(
            session=session,
            user_id=current_user.id,
            query=query,
            status=status,
            priority=priority,
            tags=tags,
            due_date_from=due_date_from,
            due_date_to=due_date_to,
            completed=completed,
            sort_by=sort_by,
            sort_order=sort_order,
            offset=offset,
            limit=limit
        )

        return search_results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.get("/tags", response_model=List[str])
async def get_user_tags(
    current_user: User = Depends(require_auth()),
    session: Session = Depends(get_session)
):
    """
    Get all unique tags used by the user
    """
    try:
        tags = TaskSearchService.get_all_tags_for_user(
            session=session,
            user_id=current_user.id
        )
        return tags
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve tags: {str(e)}")


@router.get("/filter", response_model=List[Task])
async def filter_tasks(
    status: Optional[str] = Query(None, description="Filter by status"),
    priority: Optional[PriorityEnum] = Query(None, description="Filter by priority"),
    tags: Optional[List[str]] = Query(None, description="Filter by tags"),
    due_date_from: Optional[datetime] = Query(None, description="Filter tasks with due date after this date"),
    due_date_to: Optional[datetime] = Query(None, description="Filter tasks with due date before this date"),
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    sort_by: str = Query("created_at", description="Sort by field"),
    sort_order: str = Query("desc", description="Sort order"),
    current_user: User = Depends(require_auth()),
    session: Session = Depends(get_session)
):
    """
    Filter tasks with various criteria (simpler than search, returns list of tasks)
    """
    try:
        results = TaskSearchService.search_tasks(
            session=session,
            user_id=current_user.id,
            status=status,
            priority=priority,
            tags=tags,
            due_date_from=due_date_from,
            due_date_to=due_date_to,
            completed=completed,
            sort_by=sort_by,
            sort_order=sort_order,
            offset=0,
            limit=1000  # Return all matching tasks for this endpoint
        )

        return results["tasks"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Filter failed: {str(e)}")