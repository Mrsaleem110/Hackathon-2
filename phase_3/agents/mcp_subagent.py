"""
MCP Subagent for Official MCP Server
This subagent utilizes the official MCP server skills to perform various tasks
"""

import asyncio
import json
from typing import Dict, Any, Optional, List
from pathlib import Path

# Import the MCP skills
from skills.mcp.official_server_skills import (
    get_project_file,
    put_project_file,
    list_project_dir,
    get_sys_info,
    exec_shell_cmd,
    create_proj_structure
)


class McpSubagent:
    """
    A subagent that utilizes the official MCP server skills to perform various tasks.
    This agent can read/write files, execute commands, manage projects, and interact
    with the system through the secure MCP server interface.
    """

    def __init__(self, name: str = "mcp-subagent", verbose: bool = True):
        self.name = name
        self.verbose = verbose
        self.conversation_history = []
        self.working_directory = Path.cwd()

    async def process_request(self, request: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process a request using MCP server skills.

        Args:
            request: Natural language request to process
            context: Additional context for the request

        Returns:
            Dictionary containing the result of processing
        """
        if context is None:
            context = {}

        self._log(f"Processing request: {request}")

        # Parse the request to determine the appropriate action
        parsed_action = await self._parse_request(request)

        if parsed_action["action"] == "read_file":
            return await self._handle_read_file(parsed_action)
        elif parsed_action["action"] == "write_file":
            return await self._handle_write_file(parsed_action)
        elif parsed_action["action"] == "list_directory":
            return await self._handle_list_directory(parsed_action)
        elif parsed_action["action"] == "execute_command":
            return await self._handle_execute_command(parsed_action)
        elif parsed_action["action"] == "get_system_info":
            return await self._handle_get_system_info(parsed_action)
        elif parsed_action["action"] == "create_project":
            return await self._handle_create_project(parsed_action)
        else:
            return {
                "status": "error",
                "message": f"Unknown action: {parsed_action['action']}",
                "request": request
            }

    async def _parse_request(self, request: str) -> Dict[str, Any]:
        """
        Parse a natural language request to determine the appropriate action.

        Args:
            request: Natural language request

        Returns:
            Dictionary containing the parsed action and parameters
        """
        request_lower = request.lower()

        # Determine the action based on keywords
        if any(keyword in request_lower for keyword in ["read", "show", "display", "get", "view", "content of"]):
            # Look for file path in the request
            import re
            file_match = re.search(r'(?:file|path)\s+([^\s]+)', request)
            if file_match:
                return {
                    "action": "read_file",
                    "file_path": file_match.group(1)
                }
            elif any(ext in request_lower for ext in [".py", ".txt", ".json", ".md", ".js", ".html", ".css"]):
                # Extract potential file path
                words = request.split()
                for word in words:
                    if any(ext in word for ext in [".py", ".txt", ".json", ".md", ".js", ".html", ".css"]):
                        return {
                            "action": "read_file",
                            "file_path": word
                        }

        elif any(keyword in request_lower for keyword in ["write", "create", "save", "update", "modify"]):
            # Look for file path and content
            import re
            file_match = re.search(r'(?:file|path)\s+([^\s]+)', request)
            content_match = re.search(r'content\s+(.+)', request, re.IGNORECASE)

            if file_match:
                return {
                    "action": "write_file",
                    "file_path": file_match.group(1),
                    "content": content_match.group(1) if content_match else "Default content"
                }

        elif any(keyword in request_lower for keyword in ["list", "show", "directory", "folder", "files"]):
            # Look for directory path
            import re
            dir_match = re.search(r'(?:directory|folder|path)\s+([^\s]+)', request)
            return {
                "action": "list_directory",
                "directory_path": dir_match.group(1) if dir_match else "."
            }

        elif any(keyword in request_lower for keyword in ["run", "execute", "command", "shell", "cmd"]):
            # Extract command
            import re
            cmd_match = re.search(r'(?:command|run|execute)\s+(.+)', request, re.IGNORECASE)
            if cmd_match:
                return {
                    "action": "execute_command",
                    "command": cmd_match.group(1)
                }

        elif any(keyword in request_lower for keyword in ["system", "info", "information", "environment"]):
            return {
                "action": "get_system_info"
            }

        elif any(keyword in request_lower for keyword in ["project", "structure", "setup", "initialize"]):
            return {
                "action": "create_project",
                "project_name": "new_project",
                "structure": {}
            }

        # Default to unknown action
        return {
            "action": "unknown",
            "original_request": request
        }

    async def _handle_read_file(self, action_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle read file requests."""
        file_path = action_data.get("file_path", "")

        if not file_path:
            return {
                "status": "error",
                "message": "No file path provided for read operation"
            }

        self._log(f"Reading file: {file_path}")
        result = await get_project_file(file_path)

        return {
            "status": "success" if "error" not in result else "error",
            "action": "read_file",
            "file_path": file_path,
            "result": result
        }

    async def _handle_write_file(self, action_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle write file requests."""
        file_path = action_data.get("file_path", "")
        content = action_data.get("content", "")

        if not file_path:
            return {
                "status": "error",
                "message": "No file path provided for write operation"
            }

        if not content:
            return {
                "status": "error",
                "message": "No content provided for write operation"
            }

        self._log(f"Writing to file: {file_path}")
        result = await put_project_file(file_path, content)

        return {
            "status": "success" if "error" not in result else "error",
            "action": "write_file",
            "file_path": file_path,
            "content_length": len(content),
            "result": result
        }

    async def _handle_list_directory(self, action_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle list directory requests."""
        directory_path = action_data.get("directory_path", ".")

        self._log(f"Listing directory: {directory_path}")
        result = await list_project_dir(directory_path)

        return {
            "status": "success" if "error" not in result else "error",
            "action": "list_directory",
            "directory_path": directory_path,
            "result": result
        }

    async def _handle_execute_command(self, action_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle execute command requests."""
        command = action_data.get("command", "")

        if not command:
            return {
                "status": "error",
                "message": "No command provided for execution"
            }

        self._log(f"Executing command: {command}")
        result = await exec_shell_cmd(command)

        return {
            "status": "success" if "error" not in result else "error",
            "action": "execute_command",
            "command": command,
            "result": result
        }

    async def _handle_get_system_info(self, action_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get system info requests."""
        self._log("Getting system information")
        result = await get_sys_info()

        return {
            "status": "success" if "error" not in result else "error",
            "action": "get_system_info",
            "result": result
        }

    async def _handle_create_project(self, action_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle create project requests."""
        project_name = action_data.get("project_name", "new_project")
        structure = action_data.get("structure", {})

        if not structure:
            # Provide a default project structure
            structure = {
                "README.md": "# New Project\n\nThis is a new project.",
                "src": {
                    "__init__.py": "",
                    "main.py": "# Main module\n\ndef main():\n    print('Hello, World!')\n\nif __name__ == '__main__':\n    main()"
                },
                "tests": {
                    "__init__.py": "",
                    "test_main.py": "# Tests for main module\n\nimport unittest\n\n\nclass TestMain(unittest.TestCase):\n    def test_main(self):\n        self.assertTrue(True)\n\nif __name__ == '__main__':\n    unittest.main()"
                },
                "requirements.txt": "# Project dependencies\n",
                ".gitignore": "*.pyc\n__pycache__/\n.env\n.DS_Store\n"
            }

        self._log(f"Creating project: {project_name} with structure")
        result = await create_proj_structure(project_name, structure)

        return {
            "status": "success" if "error" not in result else "error",
            "action": "create_project",
            "project_name": project_name,
            "result": result
        }

    def _log(self, message: str):
        """Log a message if verbose mode is enabled."""
        if self.verbose:
            print(f"[{self.name}] {message}")

    async def chat(self, message: str) -> str:
        """
        Chat interface for the MCP subagent.

        Args:
            message: User message to process

        Returns:
            Response from the subagent
        """
        result = await self.process_request(message)

        # Format the response
        if result["status"] == "success":
            if result["action"] == "read_file":
                content = result["result"].get("content", "No content found")
                response = f"I've read the file for you. Here's the content:\n\n{content[:1000]}..." if len(content) > 1000 else f"I've read the file for you. Here's the content:\n\n{content}"
            elif result["action"] == "write_file":
                success = result["result"].get("success", False)
                response = f"I've {'successfully' if success else 'failed to'} written to the file."
            elif result["action"] == "list_directory":
                files = result["result"].get("files", [])
                response = f"I found the following items in the directory:\n" + "\n".join(f"- {item}" for item in files[:20])  # Limit to 20 items
                if len(files) > 20:
                    response += f"\n... and {len(files) - 20} more items."
            elif result["action"] == "execute_command":
                stdout = result["result"].get("stdout", "")
                stderr = result["result"].get("stderr", "")
                return_code = result["result"].get("return_code", 0)

                if stderr:
                    response = f"Command executed with errors:\nSTDERR: {stderr}\nReturn code: {return_code}"
                else:
                    response = f"Command executed successfully:\nSTDOUT: {stdout[:500]}..." if len(stdout) > 500 else f"Command executed successfully:\nSTDOUT: {stdout}"
            elif result["action"] == "get_system_info":
                sys_info = result["result"]
                response = f"System Information:\nOS: {sys_info.get('os', 'Unknown')}\nPython: {sys_info.get('python_version', 'Unknown')}\nDirectory: {sys_info.get('current_directory', 'Unknown')}"
            elif result["action"] == "create_project":
                success = result["result"].get("success", False)
                response = f"I've {'successfully' if success else 'failed to'} created the project structure."
            else:
                response = f"Action completed: {result}"
        else:
            error_msg = result["result"].get("error", "Unknown error") if "result" in result else "Unknown error"
            response = f"I encountered an error: {error_msg}"

        return response

    async def run_interactive(self):
        """Run the subagent in interactive mode."""
        print(f"🚀 Starting {self.name} (type 'quit' to exit)")
        print("=" * 50)

        while True:
            try:
                user_input = input(f"\n{self.name}> ").strip()

                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break

                if not user_input:
                    continue

                response = await self.chat(user_input)
                print(f"\n{self.name} response: {response}")

            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")


# Example usage and testing
async def main():
    """Example of using the MCP subagent."""
    print("🎮 MCP Subagent Demo")
    print("=" * 40)

    # Create the subagent
    agent = McpSubagent("demo-agent", verbose=True)

    # Test various capabilities
    print("\n1. Getting system info...")
    response = await agent.chat("What system information can you provide?")
    print(f"Response: {response}")

    print("\n2. Listing current directory...")
    response = await agent.chat("List files in the current directory")
    print(f"Response: {response}")

    print("\n3. Creating a test file...")
    response = await agent.chat("Create a file called 'test_demo.txt' with content 'This is a demo of the MCP subagent.'")
    print(f"Response: {response}")

    print("\n4. Reading the test file...")
    response = await agent.chat("Read the content of test_demo.txt")
    print(f"Response: {response}")

    print("\n5. Executing a command...")
    response = await agent.chat("Execute command: echo 'Hello from MCP subagent!'")
    print(f"Response: {response}")

    print("\n✅ Demo completed!")


if __name__ == "__main__":
    # Run the demo
    asyncio.run(main())