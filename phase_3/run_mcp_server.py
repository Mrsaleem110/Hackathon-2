#!/usr/bin/env python3
"""
Launch script for the Official MCP Server
"""
import subprocess
import sys
import os
from pathlib import Path


def main():
    """Launch the MCP server."""
    print("Launching Official MCP Server")
    print("=" * 40)

    # Change to the project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)

    # Install dependencies if needed
    print("[Installing dependencies...]")
    result = subprocess.run([
        sys.executable, "-m", "pip", "install", "-r", "mcp/requirements.txt"
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Warning: Dependency installation had issues:")
        print(result.stderr)

    print("[Dependencies installed]")

    # Run the main server
    print("\nStarting MCP Server...")
    print("Press Ctrl+C to stop the server")
    print("-" * 40)

    # Execute the main server script
    try:
        subprocess.run([sys.executable, "mcp/src/server/main.py"], check=True)
    except KeyboardInterrupt:
        print("\n\n🛑 MCP Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ MCP Server failed to start: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()