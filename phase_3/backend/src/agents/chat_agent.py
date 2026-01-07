"""
AI Chat Agent for the Todo Chatbot using OpenAI Agents SDK.
"""
import os
from typing import Dict, List, Any, Optional
from pydantic import BaseModel
from dotenv import load_dotenv
from datetime import datetime

# Import OpenAI Agents SDK
from openai import OpenAI

# Load environment variables
load_dotenv()

class ChatAgent:
    """
    AI Agent that processes natural language requests and maps them to appropriate MCP tools.
    Uses OpenAI Agents SDK for advanced AI capabilities.
    """

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

        # Define the tools available to the agent
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Add a new task for the user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user's ID"},
                            "title": {"type": "string", "description": "The title of the task"},
                            "description": {"type": "string", "description": "The description of the task"}
                        },
                        "required": ["user_id", "title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "List all tasks for the user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user's ID"}
                        },
                        "required": ["user_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "complete_task",
                    "description": "Mark a task as completed",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user's ID"},
                            "task_id": {"type": "string", "description": "The ID of the task to complete"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Delete a task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user's ID"},
                            "task_id": {"type": "string", "description": "The ID of the task to delete"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Update a task's details",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user's ID"},
                            "task_id": {"type": "string", "description": "The ID of the task to update"},
                            "title": {"type": "string", "description": "The new title of the task"},
                            "description": {"type": "string", "description": "The new description of the task"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            }
        ]

    def process_message(self, user_message: str, user_id: str, conversation_history: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """
        Process a user message and return the AI response along with any tool calls.
        Uses OpenAI's function calling capabilities.
        """
        try:
            # Prepare the messages for the API call
            messages = []

            # Add system message to guide the AI
            messages.append({
                "role": "system",
                "content": "You are a helpful assistant that manages todo tasks. "
                          "When users request to add, list, complete, update, or delete tasks, "
                          "use the appropriate tools. Always be friendly and confirm actions to the user."
            })

            # Add conversation history if provided
            if conversation_history:
                for msg in conversation_history:
                    messages.append({
                        "role": msg.get("role", "user"),
                        "content": msg.get("content", "")
                    })

            # Add the current user message
            messages.append({
                "role": "user",
                "content": user_message
            })

            # Call the OpenAI API with function calling
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools,
                tool_choice="auto"
            )

            # Extract the response
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

            # Prepare the result
            result = {
                "conversation_id": None,  # Will be set by the calling function
                "response": response_message.content or "I processed your request.",
                "tool_calls": []
            }

            # If there are tool calls, format them
            if tool_calls:
                for tool_call in tool_calls:
                    import json
                    tool_call_dict = {
                        "name": tool_call.function.name,
                        "arguments": json.loads(tool_call.function.arguments)
                    }
                    # Ensure user_id is included in the arguments
                    if "user_id" not in tool_call_dict["arguments"]:
                        tool_call_dict["arguments"]["user_id"] = user_id
                    result["tool_calls"].append(tool_call_dict)

            return result

        except Exception as e:
            return {
                "conversation_id": None,
                "response": f"Sorry, I encountered an error processing your request: {str(e)}",
                "tool_calls": []
            }

    def generate_confirmation_message(self, tool_name: str, tool_args: Dict[str, Any]) -> str:
        """
        Generate a confirmation message based on the tool executed.
        """
        if tool_name == "add_task":
            title = tool_args.get("title", "a task")
            return f"I've added the task '{title}' to your list."
        elif tool_name == "list_tasks":
            return "I've retrieved your task list."
        elif tool_name == "complete_task":
            return "I've marked that task as completed."
        elif tool_name == "delete_task":
            return "I've deleted that task from your list."
        elif tool_name == "update_task":
            title = tool_args.get("title", "the task")
            return f"I've updated the task to '{title}'."
        else:
            return "I've processed your request."