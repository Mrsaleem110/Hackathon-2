#!/usr/bin/env python3
"""
Standalone script to run the OpenAI ChatKit UI Agent without server dependencies
"""
import asyncio
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatKitAgent:
    """
    Standalone OpenAI ChatKit UI Agent without server dependencies
    """
    def __init__(self):
        self.agent_id = str(uuid.uuid4())
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.name = "openai_chatkit_ui_agent"
        self.description = "OpenAI ChatKit UI Implementer - Handles ChatKit session management and UI integration"
        self.capabilities = [
            "create-chatkit-session",
            "refresh-chatkit-session",
            "get-workflow-details",
            "manage-client-secrets",
            "embed-chatkit-ui"
        ]

    async def create_session(self, workflow_id: str, user_id: str, metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """Create a new ChatKit session"""
        try:
            import jwt
            import time

            session_id = str(uuid.uuid4())

            payload = {
                "session_id": session_id,
                "user_id": user_id,
                "workflow_id": workflow_id,
                "iat": int(time.time()),
                "exp": int(time.time()) + (60 * 60),  # 1 hour expiry
                "iss": "openai-chatkit-agent",
                "sub": f"session:{session_id}",
                "permissions": ["read", "write"]
            }

            if metadata:
                payload.update(metadata)

            client_secret = jwt.encode(
                payload,
                "your-secret-key-here",  # In production, use environment variable
                algorithm="HS256"
            )

            session_data = {
                "session_id": session_id,
                "client_secret": client_secret,
                "workflow_id": workflow_id,
                "user_id": user_id,
                "created_at": datetime.utcnow().isoformat(),
                "expires_at": (datetime.utcnow().timestamp() + 3600),
                "metadata": metadata
            }

            self.sessions[session_id] = session_data
            logger.info(f"Created ChatKit session: {session_id}")

            return {
                "success": True,
                "session_data": session_data
            }

        except Exception as e:
            logger.error(f"Failed to create ChatKit session: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    async def refresh_session(self, session_id: str) -> Dict[str, Any]:
        """Refresh an existing ChatKit session"""
        try:
            if session_id not in self.sessions:
                return {
                    "success": False,
                    "error": "Session not found"
                }

            session_data = self.sessions[session_id]

            import jwt
            import time

            payload = {
                "session_id": session_id,
                "user_id": session_data["user_id"],
                "workflow_id": session_data["workflow_id"],
                "iat": int(time.time()),
                "exp": int(time.time()) + (60 * 60),  # 1 hour expiry
                "iss": "openai-chatkit-agent",
                "sub": f"session:{session_id}",
                "permissions": ["read", "write"]
            }

            client_secret = jwt.encode(
                payload,
                "your-secret-key-here",  # In production, use environment variable
                algorithm="HS256"
            )

            session_data["client_secret"] = client_secret
            session_data["refreshed_at"] = datetime.utcnow().isoformat()
            session_data["expires_at"] = (datetime.utcnow().timestamp() + 3600)

            self.sessions[session_id] = session_data
            logger.info(f"Refreshed ChatKit session: {session_id}")

            return {
                "success": True,
                "session_data": session_data
            }

        except Exception as e:
            logger.error(f"Failed to refresh ChatKit session: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    async def handle_task(self, task_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming tasks for the ChatKit agent"""
        try:
            if task_name == "create_session":
                workflow_id = arguments.get("workflow_id")
                user_id = arguments.get("user_id")
                metadata = arguments.get("metadata", {})

                if not workflow_id or not user_id:
                    return {
                        "success": False,
                        "error": "workflow_id and user_id are required"
                    }

                return await self.create_session(workflow_id, user_id, metadata)

            elif task_name == "refresh_session":
                session_id = arguments.get("session_id")
                if not session_id:
                    return {"success": False, "error": "session_id is required"}
                return await self.refresh_session(session_id)

            elif task_name == "get_workflow_details":
                workflow_id = arguments.get("workflow_id")
                if not workflow_id:
                    return {"success": False, "error": "workflow_id is required"}

                return {
                    "success": True,
                    "workflow": {
                        "workflow_id": workflow_id,
                        "name": f"Workflow {workflow_id}",
                        "description": "OpenAI-hosted agent workflow",
                        "status": "active",
                        "capabilities": ["text-generation", "function-calling", "file-processing"],
                        "created_at": datetime.utcnow().isoformat()
                    }
                }

            else:
                return {
                    "success": False,
                    "error": f"Unknown task: {task_name}"
                }

        except Exception as e:
            logger.error(f"Error handling task {task_name}: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

async def run_standalone_chatkit_agent():
    """
    Run the OpenAI ChatKit UI Agent as a standalone component
    """
    print("Initializing Standalone OpenAI ChatKit UI Agent...")
    print("=" * 60)

    # Create the agent instance
    agent = ChatKitAgent()

    print("+ OpenAI ChatKit UI Agent initialized successfully!")
    print(f"  - Agent ID: {agent.agent_id}")
    print(f"  - Agent Name: {agent.name}")
    print(f"  - Capabilities: {len(agent.capabilities)}")
    for cap in agent.capabilities:
        print(f"    * {cap}")

    # Demonstrate the agent functionality
    print("\nDemonstrating agent functionality:")

    # Create a session
    result = await agent.create_session("test-workflow-123", "test-user-456", {"test": True})
    if result["success"]:
        session_data = result["session_data"]
        print(f"  + Created session: {session_data['session_id']}")
        print(f"  + Client secret length: {len(session_data['client_secret'])} chars")
    else:
        print(f"  X Failed to create session: {result['error']}")

    # Refresh the session if it was created
    if result["success"]:
        session_id = session_data["session_id"]
        refresh_result = await agent.refresh_session(session_id)
        if refresh_result["success"]:
            print(f"  + Refreshed session: {session_id}")
        else:
            print(f"  X Failed to refresh session: {refresh_result['error']}")

    print("\n+ OpenAI ChatKit UI Agent is ready to handle requests!")
    print("Use the agent instance to call create_session(), refresh_session(), or handle_task() methods.")

    return agent

if __name__ == "__main__":
    try:
        agent = asyncio.run(run_standalone_chatkit_agent())
        print("\nAgent is running and ready to handle requests!")
    except Exception as e:
        print(f"\nX Error running OpenAI ChatKit UI Agent: {e}")
        import traceback
        traceback.print_exc()