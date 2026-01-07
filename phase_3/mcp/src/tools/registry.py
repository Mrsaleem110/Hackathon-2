"""
Tool registration framework for the MCP server using the mock MCP SDK.
"""
from typing import Dict, Callable, Any, Awaitable
from pydantic import BaseModel
import asyncio

class ToolRegistry:
    """Registry for managing MCP tools using the mock MCP SDK."""

    def __init__(self):
        self._tools: Dict[str, Callable] = {}
        self._schemas: Dict[str, BaseModel] = {}

    def register_tool(self, name: str, func: Callable, schema: BaseModel = None):
        """Register a new tool with the registry using the mock MCP SDK."""
        self._tools[name] = func
        if schema:
            self._schemas[name] = schema

    async def execute_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a registered tool with the given arguments using the mock MCP SDK."""
        if name not in self._tools:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Unknown tool: {name}"
                    }
                ],
                "is_error": True
            }

        try:
            # Execute the tool function using the mock MCP SDK
            result = await self._tools[name](arguments)
            return result
        except Exception as e:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Error executing tool {name}: {str(e)}"
                    }
                ],
                "is_error": True
            }

    def get_tool_names(self) -> list:
        """Get a list of all registered tool names using the mock MCP SDK."""
        return list(self._tools.keys())

    def get_tool_schema(self, name: str) -> BaseModel:
        """Get the schema for a specific tool using the mock MCP SDK."""
        return self._schemas.get(name)

# Global tool registry instance using the mock MCP SDK
tool_registry = ToolRegistry()

# Convenience decorators using the mock MCP SDK
def register_tool(name: str, schema: BaseModel = None):
    """Decorator to register a tool function using the mock MCP SDK."""
    def decorator(func: Callable) -> Callable:
        tool_registry.register_tool(name, func, schema)
        return func
    return decorator

# Example usage:
# @register_tool("add_task")
# async def add_task_impl(arguments: dict):
#     # Implementation here using the mock MCP SDK
#     pass