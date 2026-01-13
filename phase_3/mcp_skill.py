"""
MCP Server Skill Implementation
This skill demonstrates how to create and use an MCP (Model Context Protocol) server
to expose tools and context to language models.
"""

import asyncio
import os
from pathlib import Path
from typing import Optional, Dict, Any

from agents import Agent, Runner
from agents.mcp import MCPServerStdio, MCPServerStreamableHttp, MCPServerSse
from agents.model_settings import ModelSettings
from agents.types import Tool


class MCPSkill:
    """
    A skill that demonstrates different MCP server implementations
    """

    def __init__(self):
        self.name = "mcp_server_skill"

    async def create_stdio_server(self, samples_dir: Optional[Path] = None):
        """
        Creates an stdio MCP server (for local subprocess servers)
        """
        if samples_dir is None:
            samples_dir = Path.cwd()

        server = MCPServerStdio(
            name="Filesystem Server via npx",
            params={
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem", str(samples_dir)],
            },
        )
        return server

    async def create_streamable_http_server(self, server_url: str, token: Optional[str] = None):
        """
        Creates a streamable HTTP MCP server
        """
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        server = MCPServerStreamableHttp(
            name="Streamable HTTP Server",
            params={
                "url": server_url,
                "headers": headers,
                "timeout": 30,
            },
            cache_tools_list=True,
            max_retry_attempts=3,
        )
        return server

    async def create_sse_server(self, server_url: str, headers: Optional[Dict[str, str]] = None):
        """
        Creates an HTTP with SSE MCP server
        """
        if headers is None:
            headers = {}

        server = MCPServerSse(
            name="SSE Server",
            params={
                "url": server_url,
                "headers": headers,
            },
            cache_tools_list=True,
        )
        return server

    async def create_hosted_server_agent(self, server_label: str, server_url: str):
        """
        Creates an agent that uses a hosted MCP server
        """
        from agents import HostedMCPTool

        agent = Agent(
            name="MCP Hosted Assistant",
            tools=[
                HostedMCPTool(
                    tool_config={
                        "type": "mcp",
                        "server_label": server_label,
                        "server_url": server_url,
                        "require_approval": "never",
                    }
                )
            ],
        )
        return agent

    async def run_with_stdio_server(self, samples_dir: Optional[Path] = None, query: str = "List the files available to you."):
        """
        Demonstrates using an stdio MCP server with an agent
        """
        server = await self.create_stdio_server(samples_dir)

        async with server:
            agent = Agent(
                name="MCP Stdio Assistant",
                instructions="Use the MCP tools to answer the questions.",
                mcp_servers=[server],
                model_settings=ModelSettings(tool_choice="auto"),
            )

            result = await Runner.run(agent, query)
            return result.final_output

    async def run_with_streamable_http_server(self, server_url: str, token: Optional[str] = None, query: str = "What can you do?"):
        """
        Demonstrates using a streamable HTTP MCP server with an agent
        """
        server = await self.create_streamable_http_server(server_url, token)

        async with server:
            agent = Agent(
                name="MCP HTTP Assistant",
                instructions="Use the MCP tools to answer the questions.",
                mcp_servers=[server],
                model_settings=ModelSettings(tool_choice="auto"),
            )

            result = await Runner.run(agent, query)
            return result.final_output

    async def run_with_sse_server(self, server_url: str, headers: Optional[Dict[str, str]] = None, query: str = "What can you do?"):
        """
        Demonstrates using an SSE MCP server with an agent
        """
        server = await self.create_sse_server(server_url, headers)

        async with server:
            agent = Agent(
                name="MCP SSE Assistant",
                instructions="Use the MCP tools to answer the questions.",
                mcp_servers=[server],
                model_settings=ModelSettings(tool_choice="auto"),
            )

            result = await Runner.run(agent, query)
            return result.final_output

    def create_approval_function(self, safe_tools: set = None):
        """
        Creates an approval function for tool approval flows
        """
        if safe_tools is None:
            safe_tools = {"read_file", "list_directory"}

        def approve_tool(request):
            from agents import MCPToolApprovalFunctionResult

            if request.data.name in safe_tools:
                return {"approve": True}
            return {"approve": False, "reason": f"Tool {request.data.name} requires manual approval"}

        return approve_tool


# Example usage
async def main():
    """
    Example demonstrating how to use the MCP skill
    """
    mcp_skill = MCPSkill()

    print("MCP Server Skill Demo")
    print("=" * 30)

    # Example 1: Using stdio server (requires npx and @modelcontextprotocol/server-filesystem)
    try:
        print("\n1. Testing stdio server...")
        result = await mcp_skill.run_with_stdio_server(query="What files are in the current directory?")
        print(f"Result: {result}")
    except Exception as e:
        print(f"Stdio server test failed (might need npx): {e}")

    # Example 2: Create a sample agent with hosted MCP server
    print("\n2. Creating hosted server agent...")
    try:
        agent = await mcp_skill.create_hosted_server_agent(
            server_label="example_server",
            server_url="https://example-mcp-server.com"
        )
        print(f"Agent created: {agent.name}")
    except Exception as e:
        print(f"Hosted server agent creation failed: {e}")

    print("\nMCP Skill initialized successfully!")


if __name__ == "__main__":
    asyncio.run(main())