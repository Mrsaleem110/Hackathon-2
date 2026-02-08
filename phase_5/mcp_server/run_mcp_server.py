#!/usr/bin/env python3
"""
MCP Server Entry Point for Docker Container
"""
import asyncio
import uvicorn
from official_server import SampleMcpServer
import sys
import os
from fastapi import FastAPI

# Create a simple FastAPI app for health checks
app = FastAPI(title="MCP Server")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "mcp-server"}

# Global server instance
server_instance = None

async def initialize_server():
    global server_instance
    print("Initializing MCP Server...")
    server_instance = SampleMcpServer()

    try:
        await server_instance.connect()
        print("MCP Server connected successfully!")
    except Exception as e:
        print(f"Error connecting MCP server: {e}")
        raise

@app.on_event("startup")
async def startup_event():
    await initialize_server()

@app.on_event("shutdown")
async def shutdown_event():
    global server_instance
    if server_instance:
        await server_instance.cleanup()

if __name__ == "__main__":
    # Run with uvicorn
    uvicorn.run(
        "run_mcp_server:app",
        host="0.0.0.0",
        port=8001,
        reload=False,
        log_level="info"
    )