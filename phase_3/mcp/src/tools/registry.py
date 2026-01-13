"""
Tools Registry for Official MCP Server
This module contains all the tools available through the MCP server
"""

import asyncio
import subprocess
import os
import json
from typing import Dict, Any, Optional
from pathlib import Path


class ToolsRegistry:
    """Registry of all tools available through the MCP server."""

    def __init__(self):
        self.tools = {
            "get_system_info": {
                "name": "get_system_info",
                "description": "Retrieve system information including OS, Python version, and available resources",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            "list_files": {
                "name": "list_files",
                "description": "List files in a specified directory",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Directory path to list files from"
                        }
                    },
                    "required": ["path"]
                }
            },
            "read_file": {
                "name": "read_file",
                "description": "Read the contents of a specified file",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "File path to read"
                        }
                    },
                    "required": ["path"]
                }
            },
            "write_file": {
                "name": "write_file",
                "description": "Write content to a specified file",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "File path to write to"
                        },
                        "content": {
                            "type": "string",
                            "description": "Content to write to the file"
                        }
                    },
                    "required": ["path", "content"]
                }
            },
            "execute_command": {
                "name": "execute_command",
                "description": "Execute a shell command safely",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "command": {
                            "type": "string",
                            "description": "Command to execute"
                        }
                    },
                    "required": ["command"]
                }
            }
        }

    def get_tool(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """Get a specific tool definition by name."""
        return self.tools.get(tool_name)

    def get_all_tools(self) -> Dict[str, Any]:
        """Get all available tools."""
        return self.tools

    async def execute_tool(self, tool_name: str, arguments: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a specific tool with the given arguments."""
        if arguments is None:
            arguments = {}

        try:
            if tool_name == "get_system_info":
                return await self._get_system_info()
            elif tool_name == "list_files":
                return await self._list_files(arguments.get("path", "."))
            elif tool_name == "read_file":
                return await self._read_file(arguments.get("path", ""))
            elif tool_name == "write_file":
                return await self._write_file(arguments.get("path", ""), arguments.get("content", ""))
            elif tool_name == "execute_command":
                return await self._execute_command(arguments.get("command", ""))
            else:
                return {"error": f"Unknown tool: {tool_name}"}
        except Exception as e:
            return {"error": f"Error executing tool {tool_name}: {str(e)}"}

    async def _get_system_info(self) -> Dict[str, Any]:
        """Implementation for getting system information."""
        import platform
        import psutil

        info = {
            "os": platform.system(),
            "os_version": platform.version(),
            "python_version": platform.python_version(),
            "cpu_count": psutil.cpu_count(),
            "memory_total": psutil.virtual_memory().total,
            "current_directory": os.getcwd(),
            "server_time": str(asyncio.get_event_loop().time()),
            "mcp_protocol_version": "1.0"
        }
        return {"result": info}

    async def _list_files(self, path: str) -> Dict[str, Any]:
        """Implementation for listing files in a directory."""
        try:
            abs_path = os.path.abspath(path)
            if not os.path.isdir(abs_path):
                return {"error": f"Path is not a directory: {abs_path}"}

            files = os.listdir(abs_path)
            return {
                "files": files,
                "path": abs_path,
                "absolute_path": abs_path
            }
        except PermissionError:
            return {"error": f"Permission denied accessing: {path}"}
        except Exception as e:
            return {"error": f"Error listing directory {path}: {str(e)}"}

    async def _read_file(self, path: str) -> Dict[str, Any]:
        """Implementation for reading a file."""
        try:
            abs_path = os.path.abspath(path)
            if not os.path.isfile(abs_path):
                return {"error": f"File does not exist: {abs_path}"}

            with open(abs_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return {
                "content": content,
                "path": abs_path,
                "size": len(content),
                "absolute_path": abs_path
            }
        except PermissionError:
            return {"error": f"Permission denied reading: {path}"}
        except UnicodeDecodeError:
            return {"error": f"Could not decode file as UTF-8: {path}"}
        except Exception as e:
            return {"error": f"Error reading file {path}: {str(e)}"}

    async def _write_file(self, path: str, content: str) -> Dict[str, Any]:
        """Implementation for writing to a file."""
        try:
            abs_path = os.path.abspath(path)
            dir_path = os.path.dirname(abs_path)

            # Create directory if it doesn't exist
            if dir_path and not os.path.exists(dir_path):
                os.makedirs(dir_path, exist_ok=True)

            with open(abs_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return {
                "success": True,
                "path": abs_path,
                "written_bytes": len(content),
                "absolute_path": abs_path
            }
        except PermissionError:
            return {"error": f"Permission denied writing to: {path}"}
        except Exception as e:
            return {"error": f"Error writing to file {path}: {str(e)}"}

    async def _execute_command(self, command: str) -> Dict[str, Any]:
        """Implementation for executing a shell command."""
        try:
            # Sanitize command to prevent shell injection
            if not isinstance(command, str) or not command.strip():
                return {"error": "Empty or invalid command"}

            # Prevent dangerous commands
            dangerous_commands = ["rm", "mv", "dd", "mkfs", "shutdown", "reboot", "kill", "pkill", "format", "fdisk", "del", "rmdir"]
            cmd_parts = command.split()
            if cmd_parts and cmd_parts[0] in dangerous_commands:
                return {"error": f"Command '{cmd_parts[0]}' is restricted for security reasons"}

            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30  # 30 second timeout
            )

            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode,
                "command": command
            }
        except subprocess.TimeoutExpired:
            return {"error": "Command timed out after 30 seconds"}
        except Exception as e:
            return {"error": f"Error executing command: {str(e)}"}