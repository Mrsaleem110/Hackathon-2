import asyncio
from mcp.server import Server
from mcp.types import Tool, Argument, Result
import json
from typing import Dict, Any


class TodoMCPServer:
    def __init__(self, task_service):
        self.server = Server("todo-mcp-server")
        self.task_service = task_service

        # Register tools
        self._register_tools()

    def _register_tools(self):
        """Register all MCP tools"""
        # add_task tool
        @self.server.tool("add_task")
        async def add_task(title: str, description: str = "", due_date: str = "") -> Result:
            """Add a new task to the todo list"""
            try:
                task_data = {
                    "title": title,
                    "description": description,
                    "due_date": due_date
                }
                result = await self.task_service.create_task(task_data)
                return Result(content=json.dumps(result))
            except Exception as e:
                return Result(error=str(e))

        # list_tasks tool
        @self.server.tool("list_tasks")
        async def list_tasks(status: str = "all") -> Result:
            """List tasks with optional status filter"""
            try:
                result = await self.task_service.get_tasks({"status": status})
                return Result(content=json.dumps(result))
            except Exception as e:
                return Result(error=str(e))

        # complete_task tool
        @self.server.tool("complete_task")
        async def complete_task(task_id: str) -> Result:
            """Mark a task as completed"""
            try:
                result = await self.task_service.update_task(task_id, {"status": "completed"})
                return Result(content=json.dumps(result))
            except Exception as e:
                return Result(error=str(e))

        # delete_task tool
        async def delete_task(task_id: str) -> Result:
            """Delete a task from the todo list"""
            try:
                result = await self.task_service.delete_task(task_id)
                return Result(content=json.dumps(result))
            except Exception as e:
                return Result(error=str(e))

        # update_task tool
        @self.server.tool("update_task")
        async def update_task(task_id: str, title: str = "", description: str = "", due_date: str = "", status: str = "") -> Result:
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
                return Result(content=json.dumps(result))
            except Exception as e:
                return Result(error=str(e))

        # Register the delete_task tool
        self.server.tools.append(
            Tool(
                name="delete_task",
                description="Delete a task from the todo list",
                input_schema={
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string", "description": "ID of the task to delete"}
                    },
                    "required": ["task_id"]
                }
            )
        )

    async def start(self, host: str = "localhost", port: int = 3000):
        """Start the MCP server"""
        await self.server.run_tcp(host, port)