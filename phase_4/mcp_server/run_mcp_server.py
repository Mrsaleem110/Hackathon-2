#!/usr/bin/env python3
"""
MCP Server Entry Point for Docker Container
"""
import asyncio
import uvicorn
from official_server import create_official_server

def main():
    """Main entry point for the MCP server."""
    print("Starting MCP Server...")

    # For production use with Docker, we'll run the server differently
    import sys
    import os

    # Add the current directory to the Python path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    # Import and run the official server
    from official_server import SampleMcpServer

    # Create and run the server
    server = SampleMcpServer()

    try:
        # Connect to the server
        import asyncio
        asyncio.run(server.connect())

        # Keep the server running
        print("MCP Server is running on port 8001...")
        print("Press Ctrl+C to stop")

        # Keep the event loop running
        try:
            asyncio.run(asyncio.sleep(float('inf')))
        except KeyboardInterrupt:
            print("\nShutting down...")

    except Exception as e:
        print(f"Error running MCP server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()