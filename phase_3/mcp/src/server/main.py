import asyncio
from pydantic import BaseModel
from typing import List, Dict, Any
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Mock MCP Server implementation
class MockMCPServer:
    def __init__(self, name: str):
        self.name = name
        self.tools = {}
        self.prompts = []

    def register_tool(self, name: str, func):
        self.tools[name] = func

    def register_prompt(self, prompt):
        self.prompts.append(prompt)

    async def call_tool(self, name: str, arguments: dict):
        if name in self.tools:
            return await self.tools[name](arguments)
        else:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Unknown tool: {name}"
                    }
                ],
                "is_error": True
            }

    async def serve(self, host: str, port: int):
        # This would start the actual server in a real implementation
        # For now, we'll just simulate it
        return MockServerContext(host, port)

class MockServerContext:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    async def __aenter__(self):
        print(f"Mock MCP Server running on {self.host}:{self.port}")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("Mock MCP Server shutting down")

# Initialize the mock MCP server
server = MockMCPServer("todo-chatbot-mcp-server")

# Import tool registry
from ..tools.registry import tool_registry

class TaskOperationParams(BaseModel):
    user_id: str
    title: str = ""
    description: str = ""
    task_id: str = ""

def list_prompts_decorator(func):
    """Decorator to register prompts."""
    async def wrapper():
        prompts = await func()
        for prompt in prompts:
            server.register_prompt(prompt)
        return prompts
    return wrapper

def call_tool_decorator(func):
    """Decorator to register the call tool handler."""
    async def wrapper(name: str, arguments: dict):
        return await func(name, arguments)
    return wrapper

@list_prompts_decorator
async def handle_list_prompts():
    """Return available prompts for the todo chatbot."""
    return [
        {
            "name": "add_task",
            "title": "Add a new task",
            "description": "Add a new todo task for the user"
        },
        {
            "name": "list_tasks",
            "title": "List user tasks",
            "description": "List all tasks for the user"
        },
        {
            "name": "complete_task",
            "title": "Complete a task",
            "description": "Mark a task as completed"
        },
        {
            "name": "delete_task",
            "title": "Delete a task",
            "description": "Delete a task"
        },
        {
            "name": "update_task",
            "title": "Update a task",
            "description": "Update a task's details"
        }
    ]

@call_tool_decorator
async def handle_call_tool(name: str, arguments: dict):
    """Handle tool calls from the AI agent."""
    return await tool_registry.execute_tool(name, arguments)

async def add_task(params: Dict[str, Any]):
    """Add a new task."""
    # This would normally connect to the database
    # For now, return a mock response
    user_id = params.get("user_id", "")
    title = params.get("title", "")
    description = params.get("description", "")

    return {
        "content": [
            {
                "type": "text",
                "text": f"Task '{title}' added successfully for user {user_id}"
            }
        ]
    }

async def list_tasks(params: Dict[str, Any]):
    """List tasks for a user."""
    user_id = params.get("user_id", "")

    return {
        "content": [
            {
                "type": "text",
                "text": f"Tasks for user {user_id}: [Sample Task 1, Sample Task 2]"
            }
        ]
    }

async def complete_task(params: Dict[str, Any]):
    """Mark a task as completed."""
    user_id = params.get("user_id", "")
    task_id = params.get("task_id", "")

    return {
        "content": [
            {
                "type": "text",
                "text": f"Task {task_id} marked as completed for user {user_id}"
            }
        ]
    }

async def delete_task(params: Dict[str, Any]):
    """Delete a task."""
    user_id = params.get("user_id", "")
    task_id = params.get("task_id", "")

    return {
        "content": [
            {
                "type": "text",
                "text": f"Task {task_id} deleted for user {user_id}"
            }
        ]
    }

async def update_task(params: Dict[str, Any]):
    """Update a task."""
    user_id = params.get("user_id", "")
    task_id = params.get("task_id", "")
    title = params.get("title", "")
    description = params.get("description", "")

    return {
        "content": [
            {
                "type": "text",
                "text": f"Task {task_id} updated for user {user_id} with title '{title}'"
            }
        ]
    }

# Register the tools with the registry
tool_registry.register_tool("add_task", add_task)
tool_registry.register_tool("list_tasks", list_tasks)
tool_registry.register_tool("complete_task", complete_task)
tool_registry.register_tool("delete_task", delete_task)
tool_registry.register_tool("update_task", update_task)

async def main():
    """Start the MCP server."""
    print(f"MCP Server running on {os.getenv('MCP_HOST', 'localhost')}:{os.getenv('MCP_PORT', '3000')}")
    await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())