"""
Configuration module for the MCP server.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration settings
MCP_HOST = os.getenv("MCP_HOST", "localhost")
MCP_PORT = int(os.getenv("MCP_PORT", "3000"))
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost:5432/todo_chatbot")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Task validation settings
MAX_TITLE_LENGTH = 255
MAX_DESCRIPTION_LENGTH = 1000