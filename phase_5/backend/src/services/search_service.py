from typing import List, Optional, Dict, Any
from sqlmodel import Session, select, and_, or_, func
from datetime import datetime
from ..models.task import Task
from enum import Enum


class PriorityEnum(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TaskSearchService:
    @staticmethod
    def search_tasks(
        session: Session,
        user_id: str,
        query: Optional[str] = None,
        status: Optional[str] = None,
        priority: Optional[PriorityEnum] = None,
        tags: Optional[List[str]] = None,
        due_date_from: Optional[datetime] = None,
        due_date_to: Optional[datetime] = None,
        completed: Optional[bool] = None,
        sort_by: Optional[str] = "created_at",  # created_at, due_date, priority
        sort_order: Optional[str] = "desc",  # asc or desc
        offset: Optional[int] = 0,
        limit: Optional[int] = 100
    ) -> Dict[str, Any]:
        """
        Search and filter tasks with multiple criteria
        """
        # Base query for user's tasks
        statement = select(Task).where(Task.user_id == user_id)

        # Apply text search on title and description
        if query:
            statement = statement.where(
                or_(
                    Task.title.ilike(f"%{query}%"),
                    Task.description.ilike(f"%{query}%")
                )
            )

        # Apply status filter
        if status:
            statement = statement.where(Task.status == status)

        # Apply priority filter
        if priority:
            statement = statement.where(Task.priority == priority)

        # Apply completion filter
        if completed is not None:
            statement = statement.where(Task.completed == completed)

        # Apply due date range filter
        if due_date_from:
            statement = statement.where(Task.due_date >= due_date_from)
        if due_date_to:
            statement = statement.where(Task.due_date <= due_date_to)

        # Apply sorting
        if sort_by == "due_date":
            if sort_order == "asc":
                statement = statement.order_by(Task.due_date)
            else:
                statement = statement.order_by(Task.due_date.desc())
        elif sort_by == "priority":
            if sort_order == "asc":
                # Sort order: low, medium, high
                priority_order = func.array_position(
                    func.array(['low', 'medium', 'high']),
                    Task.priority
                )
                statement = statement.order_by(priority_order)
            else:
                # Reverse order: high, medium, low
                priority_order = func.array_position(
                    func.array(['high', 'medium', 'low']),
                    Task.priority
                )
                statement = statement.order_by(priority_order)
        elif sort_by == "created_at":
            if sort_order == "asc":
                statement = statement.order_by(Task.created_at)
            else:
                statement = statement.order_by(Task.created_at.desc())
        else:  # Default sorting by creation date, newest first
            statement = statement.order_by(Task.created_at.desc())

        # Apply pagination
        statement = statement.offset(offset).limit(limit)

        # Execute query
        results = session.exec(statement).all()

        # Get total count for pagination info
        count_statement = select(func.count(Task.id)).where(Task.user_id == user_id)

        # Apply same filters for count
        if query:
            count_statement = count_statement.where(
                or_(
                    Task.title.ilike(f"%{query}%"),
                    Task.description.ilike(f"%{query}%")
                )
            )
        if status:
            count_statement = count_statement.where(Task.status == status)
        if priority:
            count_statement = count_statement.where(Task.priority == priority)
        if completed is not None:
            count_statement = count_statement.where(Task.completed == completed)
        if due_date_from:
            count_statement = count_statement.where(Task.due_date >= due_date_from)
        if due_date_to:
            count_statement = count_statement.where(Task.due_date <= due_date_to)

        total_count = session.exec(count_statement).one()

        return {
            "tasks": results,
            "total_count": total_count,
            "offset": offset,
            "limit": limit,
            "has_more": len(results) == limit and (offset + limit) < total_count
        }

    @staticmethod
    def get_tasks_by_tags(
        session: Session,
        user_id: str,
        tag_names: List[str]
    ) -> List[Task]:
        """
        Get tasks that have any of the specified tags
        """
        statement = select(Task).where(
            and_(
                Task.user_id == user_id,
                # Since tags are stored as array in the task model, we'll search in the tags array
                # For each tag, check if it exists in the task's tags array
            )
        )

        # For now, since we store tags as an array in the task model,
        # we'll filter using the array field
        for tag in tag_names:
            statement = statement.where(Task.tags.contains([tag]))

        return session.exec(statement).all()

    @staticmethod
    def get_all_tags_for_user(session: Session, user_id: str) -> List[str]:
        """
        Get all unique tags used by a user
        """
        # Get all tasks for the user
        statement = select(Task).where(Task.user_id == user_id)
        tasks = session.exec(statement).all()

        # Extract all tags from all tasks and return unique ones
        all_tags = set()
        for task in tasks:
            if task.tags:
                all_tags.update(task.tags)

        return sorted(list(all_tags))