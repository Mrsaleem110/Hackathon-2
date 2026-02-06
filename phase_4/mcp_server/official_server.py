"""
Official MCP Server Implementation
"""

import asyncio
import json
import sys
from typing import Any, Dict, List, Optional
from pathlib import Path

from src.agents.mcp.server import MCPServerStdio, MCPServerStdioParams
from src.agents.mcp.util import ToolFilterStatic
from ai.sdk.tools import Tool


class OfficialMcpServer:
    """
    Official MCP Server implementation with standard tools and capabilities.
    """

    def __init__(self, name: str = "official-mcp-server"):
        self.name = name
        self.params = MCPServerStdioParams(
            command=sys.executable,
            args=[str(Path(__file__).parent / "server_process.py")],
            env={"PYTHONPATH": str(Path.cwd())},
            cwd=str(Path.cwd()),
        )

        # Initialize the underlying stdio server
        self._server = MCPServerStdio(
            params=self.params,
            name=self.name,
            cache_tools_list=True,
            client_session_timeout_seconds=10.0
        )

    async def connect(self):
        """Connect to the MCP server."""
        await self._server.connect()

    async def cleanup(self):
        """Clean up the server connection."""
        await self._server.cleanup()

    async def list_tools(self):
        """List available tools from the server."""
        return await self._server.list_tools()

    async def call_tool(self, tool_name: str, arguments: Optional[Dict[str, Any]] = None):
        """Call a specific tool on the server."""
        return await self._server.call_tool(tool_name, arguments or {})

    @property
    def server(self):
        """Access to the underlying server instance."""
        return self._server


class SampleMcpServer(MCPServerStdio):
    """
    Sample implementation of an MCP server with predefined tools.
    This demonstrates how to create an official MCP server.
    """

    def __init__(self, name: str = "sample-official-server"):
        params = MCPServerStdioParams(
            command=sys.executable,
            args=["-c", "print('MCP Server Ready'); input()"],  # Placeholder command
        )

        super().__init__(
            params=params,
            name=name,
            cache_tools_list=True
        )

        # Define sample tools that this server will provide
        self._tools = [
            Tool(
                name="get_system_info",
                description="Retrieve system information including OS, Python version, and available resources",
                input_schema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            ),
            Tool(
                name="list_files",
                description="List files in a specified directory",
                input_schema={
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Directory path to list files from"
                        }
                    },
                    "required": ["path"]
                }
            ),
            Tool(
                name="read_file",
                description="Read the contents of a specified file",
                input_schema={
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "File path to read"
                        }
                    },
                    "required": ["path"]
                }
            )
        ]

    async def connect(self):
        """Connect to the server process."""
        # In a real implementation, this would start the actual server process
        print(f"Connecting to {self.name}...")
        await super().connect()

    async def cleanup(self):
        """Clean up server resources."""
        print(f"Cleaning up {self.name}...")
        await super().cleanup()

    async def list_tools(self):
        """Return the list of available tools."""
        return self._tools

    async def call_tool(self, tool_name: str, arguments: Optional[Dict[str, Any]] = None):
        """Handle tool calls."""
        if tool_name == "get_system_info":
            return await self._get_system_info()
        elif tool_name == "list_files":
            return await self._list_files(arguments.get("path", "."))
        elif tool_name == "read_file":
            return await self._read_file(arguments.get("path", ""))
        else:
            raise ValueError(f"Unknown tool: {tool_name}")

    async def _get_system_info(self):
        """Implementation for getting system information."""
        import platform
        import psutil
        import os

        info = {
            "os": platform.system(),
            "os_version": platform.version(),
            "python_version": platform.python_version(),
            "cpu_count": psutil.cpu_count(),
            "memory_total": psutil.virtual_memory().total,
            "disk_usage": psutil.disk_usage("/").total if os.name != "nt" else "N/A",
            "current_directory": os.getcwd()
        }
        return {"result": info}

    async def _list_files(self, path: str):
        """Implementation for listing files in a directory."""
        import os

        try:
            files = os.listdir(path)
            return {"files": files, "path": path}
        except Exception as e:
            return {"error": str(e)}

    async def _read_file(self, path: str):
        """Implementation for reading a file."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            return {"content": content, "path": path}
        except Exception as e:
            return {"error": str(e)}


async def create_official_server(name: str = "official-mcp-server") -> SampleMcpServer:
    """
    Factory function to create an instance of the official MCP server.
    """
    server = SampleMcpServer(name=name)
    return server


if __name__ == "__main__":
    # Example usage
    async def main():
        server = await create_official_server()

        try:
            await server.connect()

            # List available tools
            tools = await server.list_tools()
            print(f"Available tools: {[tool.name for tool in tools]}")

            # Test one of the tools
            result = await server.call_tool("get_system_info")
            print(f"System info: {result}")

        finally:
            await server.cleanup()

    asyncio.run(main())