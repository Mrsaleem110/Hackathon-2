"""
Official MCP Server Skills
This module provides skills for interacting with the official MCP server
"""

import asyncio
import json
from typing import Dict, Any, Optional
from pathlib import Path


class OfficialMcpSkills:
    """
    Skills for interacting with the official MCP server.
    These skills provide high-level operations that use the underlying MCP tools.
    """

    def __init__(self):
        self.skill_name = "official_mcp_skills"
        self.description = "Skills for interacting with the official MCP server"

    async def read_project_file(self, file_path: str) -> Dict[str, Any]:
        """
        Read a file from the project with error handling.

        Args:
            file_path: Path to the file to read

        Returns:
            Dictionary containing file content or error information
        """
        try:
            # Use the MCP server's read_file tool
            result = await self._call_mcp_tool("read_file", {"path": file_path})
            return result
        except Exception as e:
            return {"error": f"Failed to read file {file_path}: {str(e)}"}

    async def write_project_file(self, file_path: str, content: str) -> Dict[str, Any]:
        """
        Write content to a project file with error handling.

        Args:
            file_path: Path to the file to write
            content: Content to write to the file

        Returns:
            Dictionary containing success/error information
        """
        try:
            # Use the MCP server's write_file tool
            result = await self._call_mcp_tool("write_file", {
                "path": file_path,
                "content": content
            })
            return result
        except Exception as e:
            return {"error": f"Failed to write file {file_path}: {str(e)}"}

    async def list_project_directory(self, directory_path: str = ".") -> Dict[str, Any]:
        """
        List files in a project directory.

        Args:
            directory_path: Path to the directory to list (default: current directory)

        Returns:
            Dictionary containing list of files or error information
        """
        try:
            # Use the MCP server's list_files tool
            result = await self._call_mcp_tool("list_files", {"path": directory_path})
            return result
        except Exception as e:
            return {"error": f"Failed to list directory {directory_path}: {str(e)}"}

    async def get_system_information(self) -> Dict[str, Any]:
        """
        Get system information from the MCP server.

        Returns:
            Dictionary containing system information or error information
        """
        try:
            # Use the MCP server's get_system_info tool
            result = await self._call_mcp_tool("get_system_info", {})
            return result
        except Exception as e:
            return {"error": f"Failed to get system information: {str(e)}"}

    async def execute_shell_command(self, command: str) -> Dict[str, Any]:
        """
        Execute a shell command safely through the MCP server.

        Args:
            command: Command to execute

        Returns:
            Dictionary containing command output or error information
        """
        try:
            # Use the MCP server's execute_command tool
            result = await self._call_mcp_tool("execute_command", {"command": command})
            return result
        except Exception as e:
            return {"error": f"Failed to execute command '{command}': {str(e)}"}

    async def create_project_structure(self, project_name: str, structure: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a project structure based on the provided definition.

        Args:
            project_name: Name of the project
            structure: Dictionary defining the directory/file structure

        Returns:
            Dictionary containing success/error information
        """
        try:
            results = []

            # Create project root directory
            project_root = Path(project_name)
            project_root.mkdir(exist_ok=True)

            # Recursively create the structure
            await self._create_structure_recursive(project_root, structure)

            return {
                "success": True,
                "project_name": project_name,
                "structure": structure,
                "message": f"Project '{project_name}' structure created successfully"
            }
        except Exception as e:
            return {"error": f"Failed to create project structure: {str(e)}"}

    async def _create_structure_recursive(self, base_path: Path, structure: Dict[str, Any]):
        """Helper method to recursively create directory/file structure."""
        for name, content in structure.items():
            path = base_path / name

            if isinstance(content, dict):
                # It's a directory
                path.mkdir(exist_ok=True)
                await self._create_structure_recursive(path, content)
            elif isinstance(content, str):
                # It's a file
                path.write_text(content, encoding='utf-8')

    async def _call_mcp_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Internal method to call MCP tools.
        In a real implementation, this would communicate with the MCP server.
        For this example, we'll simulate the tool calls.
        """
        # This is a placeholder implementation
        # In a real scenario, this would make actual calls to the MCP server

        print(f"Calling MCP tool: {tool_name} with args: {arguments}")

        # Simulate different tool behaviors
        if tool_name == "read_file":
            try:
                with open(arguments["path"], 'r', encoding='utf-8') as f:
                    content = f.read()
                return {"content": content, "path": arguments["path"]}
            except Exception as e:
                return {"error": str(e)}
        elif tool_name == "write_file":
            try:
                path = Path(arguments["path"])
                path.parent.mkdir(parents=True, exist_ok=True)
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(arguments["content"])
                return {"success": True, "path": arguments["path"]}
            except Exception as e:
                return {"error": str(e)}
        elif tool_name == "list_files":
            try:
                path = Path(arguments["path"])
                files = [str(p) for p in path.iterdir()]
                return {"files": files, "path": str(path)}
            except Exception as e:
                return {"error": str(e)}
        elif tool_name == "get_system_info":
            import platform
            return {
                "os": platform.system(),
                "python_version": platform.python_version(),
                "current_directory": str(Path.cwd())
            }
        elif tool_name == "execute_command":
            import subprocess
            try:
                result = subprocess.run(
                    arguments["command"],
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                return {
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "return_code": result.returncode
                }
            except Exception as e:
                return {"error": str(e)}
        else:
            return {"error": f"Unknown tool: {tool_name}"}


# Singleton instance
official_mcp_skills = OfficialMcpSkills()


async def get_project_file(file_path: str) -> Dict[str, Any]:
    """Skill to read a project file."""
    return await official_mcp_skills.read_project_file(file_path)


async def put_project_file(file_path: str, content: str) -> Dict[str, Any]:
    """Skill to write a project file."""
    return await official_mcp_skills.write_project_file(file_path, content)


async def list_project_dir(directory_path: str = ".") -> Dict[str, Any]:
    """Skill to list a project directory."""
    return await official_mcp_skills.list_project_directory(directory_path)


async def get_sys_info() -> Dict[str, Any]:
    """Skill to get system information."""
    return await official_mcp_skills.get_system_information()


async def exec_shell_cmd(command: str) -> Dict[str, Any]:
    """Skill to execute a shell command."""
    return await official_mcp_skills.execute_shell_command(command)


async def create_proj_structure(project_name: str, structure: Dict[str, Any]) -> Dict[str, Any]:
    """Skill to create a project structure."""
    return await official_mcp_skills.create_project_structure(project_name, structure)


# Example usage
async def main():
    """Example of using the MCP skills."""
    print("Testing Official MCP Skills")
    print("=" * 40)

    # Get system info
    sys_info = await get_sys_info()
    print(f"System Info: {sys_info}")

    # List current directory
    dir_list = await list_project_dir(".")
    print(f"Current directory: {dir_list}")

    # Create a sample file
    result = await put_project_file("test_file.txt", "Hello, MCP Server!")
    print(f"File write result: {result}")

    # Read the file back
    content = await get_project_file("test_file.txt")
    print(f"File content: {content}")

    # Execute a command
    cmd_result = await exec_shell_cmd("echo 'Hello from MCP skill'")
    print(f"Command result: {cmd_result}")


if __name__ == "__main__":
    asyncio.run(main())