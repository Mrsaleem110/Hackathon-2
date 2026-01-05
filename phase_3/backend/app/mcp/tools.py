from typing import Dict, Any, List
import json


class TodoTools:
    """
    This module provides the actual implementations of the MCP tools
    These functions would be called by the MCP server
    """

    def __init__(self, task_service):
        self.task_service = task_service

    async def add_task(self, title: str, description: str = "", due_date: str = "") -> Dict[str, Any]:
        """Add a new task to the todo list"""
        try:
            task_data = {
                "title": title,
                "description": description,
                "due_date": due_date
            }
            result = await self.task_service.create_task(task_data)
            return result
        except Exception as e:
            raise e

    async def list_tasks(self, status: str = "all") -> List[Dict[str, Any]]:
        """List tasks with optional status filter"""
        try:
            result = await self.task_service.get_tasks({"status": status})
            return result
        except Exception as e:
            raise e

    async def complete_task(self, task_id: str) -> Dict[str, Any]:
        """Mark a task as completed"""
        try:
            result = await self.task_service.update_task(task_id, {"status": "completed"})
            return result
        except Exception as e:
            raise e

    async def delete_task(self, task_id: str) -> bool:
        """Delete a task from the todo list"""
        try:
            result = await self.task_service.delete_task(task_id)
            return result
        except Exception as e:
            raise e

    async def update_task(self, task_id: str, title: str = "", description: str = "", due_date: str = "", status: str = "") -> Dict[str, Any]:
        """Update an existing task"""
        try:
            update_data = {}
            if title:
                update_data["title"] = title
            if description:
                update_data["description"] = description
            if due_date:
                update_data["due_date"] = due_date
            if status:
                update_data["status"] = status

            result = await self.task_service.update_task(task_id, update_data)
            return result
        except Exception as e:
            raise e