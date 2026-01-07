"""
MCP tools for task operations in the AI-Powered Todo Chatbot using the mock MCP SDK.
"""
import asyncio
from typing import Dict, Any, List
from datetime import datetime
import uuid
from pydantic import BaseModel
from sqlmodel import create_engine, Session, select
from ..config import DATABASE_URL
import sys
import os
# Add the backend directory to the path so we can import the models and services
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", "backend"))

from src.models.task import Task, TaskCreate, TaskUpdate
from src.models.conversation import Conversation
from src.models.message import Message, MessageRole
from src.services.task_service import TaskService

# Create database engine
engine = create_engine(DATABASE_URL)

class AddTaskParams(BaseModel):
    user_id: str
    title: str
    description: str = ""

class ListTasksParams(BaseModel):
    user_id: str

class CompleteTaskParams(BaseModel):
    user_id: str
    task_id: str  # This will be the UUID string

class DeleteTaskParams(BaseModel):
    user_id: str
    task_id: str  # This will be the UUID string

class UpdateTaskParams(BaseModel):
    user_id: str
    task_id: str  # This will be the UUID string
    title: str = ""
    description: str = ""

async def add_task(params: Dict[str, Any]) -> Dict[str, Any]:
    """Add a new task for a user using the mock MCP SDK."""
    try:
        user_id = params.get("user_id")
        title = params.get("title", "")
        description = params.get("description", "")

        if not user_id or not title:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": "Error: Missing required parameters (user_id and title are required)"
                    }
                ],
                "is_error": True
            }

        # Create the task using the service
        task_create = TaskCreate(
            title=title,
            description=description,
            user_id=user_id
        )

        with Session(engine) as session:
            task = TaskService.create_task(session, task_create)

        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Task '{task.title}' added successfully."
                }
            ]
        }
    except Exception as e:
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Error adding task: {str(e)}"
                }
            ],
            "is_error": True
        }

async def list_tasks(params: Dict[str, Any]) -> Dict[str, Any]:
    """List all tasks for a user using the mock MCP SDK."""
    try:
        user_id = params.get("user_id")

        if not user_id:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": "Error: Missing required parameter (user_id is required)"
                    }
                ],
                "is_error": True
            }

        with Session(engine) as session:
            tasks = TaskService.get_tasks_by_user(session, user_id)

        if not tasks:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": "You have no tasks."
                    }
                ]
            }

        task_list = []
        for task in tasks:
            status = "✓" if task.completed else "○"
            task_list.append(f"{status} {task.title}")

        task_str = "\n".join([f"- {task}" for task in task_list])

        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Your tasks:\n{task_str}"
                }
            ]
        }
    except Exception as e:
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Error listing tasks: {str(e)}"
                }
            ],
            "is_error": True
        }

async def complete_task(params: Dict[str, Any]) -> Dict[str, Any]:
    """Mark a task as completed using the mock MCP SDK."""
    try:
        user_id = params.get("user_id")
        task_id_str = params.get("task_id")

        if not user_id or not task_id_str:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": "Error: Missing required parameters (user_id and task_id are required)"
                    }
                ],
                "is_error": True
            }

        try:
            task_id = uuid.UUID(task_id_str)
        except ValueError:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Error: Invalid task ID format: {task_id_str}"
                    }
                ],
                "is_error": True
            }

        with Session(engine) as session:
            # Verify that the task belongs to the user
            task = session.get(Task, task_id)
            if not task:
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Error: Task with ID {task_id_str} not found"
                        }
                    ],
                    "is_error": True
                }

            if task.user_id != user_id:
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": "Error: You don't have permission to modify this task"
                        }
                    ],
                    "is_error": True
                }

            # Complete the task
            completed_task = TaskService.complete_task(session, task_id)

        if completed_task:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Task '{completed_task.title}' marked as completed."
                    }
                ]
            }
        else:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Error: Could not complete task with ID {task_id_str}"
                    }
                ],
                "is_error": True
            }
    except Exception as e:
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Error completing task: {str(e)}"
                }
            ],
            "is_error": True
        }

async def delete_task(params: Dict[str, Any]) -> Dict[str, Any]:
    """Delete a task using the mock MCP SDK."""
    try:
        user_id = params.get("user_id")
        task_id_str = params.get("task_id")

        if not user_id or not task_id_str:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": "Error: Missing required parameters (user_id and task_id are required)"
                    }
                ],
                "is_error": True
            }

        try:
            task_id = uuid.UUID(task_id_str)
        except ValueError:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Error: Invalid task ID format: {task_id_str}"
                    }
                ],
                "is_error": True
            }

        with Session(engine) as session:
            # Verify that the task belongs to the user
            task = session.get(Task, task_id)
            if not task:
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Error: Task with ID {task_id_str} not found"
                        }
                    ],
                    "is_error": True
                }

            if task.user_id != user_id:
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": "Error: You don't have permission to delete this task"
                        }
                    ],
                    "is_error": True
                }

            # Delete the task
            success = TaskService.delete_task(session, task_id)

        if success:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": "Task deleted successfully."
                    }
                ]
            }
        else:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Error: Could not delete task with ID {task_id_str}"
                    }
                ],
                "is_error": True
            }
    except Exception as e:
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Error deleting task: {str(e)}"
                }
            ],
            "is_error": True
        }

async def update_task(params: Dict[str, Any]) -> Dict[str, Any]:
    """Update a task using the mock MCP SDK."""
    try:
        user_id = params.get("user_id")
        task_id_str = params.get("task_id")
        title = params.get("title", "")
        description = params.get("description", "")

        if not user_id or not task_id_str:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": "Error: Missing required parameters (user_id and task_id are required)"
                    }
                ],
                "is_error": True
            }

        # Check if at least one field to update is provided
        if not title and not description:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": "Error: At least one field (title or description) must be provided for update"
                    }
                ],
                "is_error": True
            }

        try:
            task_id = uuid.UUID(task_id_str)
        except ValueError:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Error: Invalid task ID format: {task_id_str}"
                    }
                ],
                "is_error": True
            }

        with Session(engine) as session:
            # Verify that the task belongs to the user
            task = session.get(Task, task_id)
            if not task:
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Error: Task with ID {task_id_str} not found"
                        }
                    ],
                    "is_error": True
                }

            if task.user_id != user_id:
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": "Error: You don't have permission to update this task"
                        }
                    ],
                    "is_error": True
                }

            # Prepare update data
            task_update = TaskUpdate()
            if title:
                task_update.title = title
            if description:
                task_update.description = description

            # Update the task
            updated_task = TaskService.update_task(session, task_id, task_update)

        if updated_task:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Task updated successfully to: '{updated_task.title}'"
                    }
                ]
            }
        else:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Error: Could not update task with ID {task_id_str}"
                    }
                ],
                "is_error": True
            }
    except Exception as e:
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Error updating task: {str(e)}"
                }
            ],
            "is_error": True
        }

# Register the tools with the registry using the mock MCP SDK
from .registry import register_tool

register_tool("add_task")(add_task)
register_tool("list_tasks")(list_tasks)
register_tool("complete_task")(complete_task)
register_tool("delete_task")(delete_task)
register_tool("update_task")(update_task)