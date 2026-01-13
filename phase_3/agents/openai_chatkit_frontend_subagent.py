#!/usr/bin/env python3
"""
OpenAI ChatKit Frontend Subagent
This subagent specializes in creating and managing OpenAI ChatKit frontend components.
"""
import asyncio
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
import logging
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import the OpenAI ChatKit Frontend skills
try:
    from skills.openai_chatkit_frontend.openai_chatkit_frontend_skills import (
        create_chatkit_ui_component,
        create_chatkit_hook,
        create_chatkit_session,
        generate_chatkit_integration_code,
        write_chatkit_component_to_file
    )
except ImportError as e:
    logger.warning(f"OpenAI ChatKit Frontend skills not available: {e}. Please install the skills first.")
    # Define dummy functions for testing
    async def create_chatkit_ui_component(*args, **kwargs):
        return {"success": False, "error": "Skills not available", "component_code": "// Dummy ChatKit UI component code"}
    async def create_chatkit_hook(*args, **kwargs):
        return {"success": False, "error": "Skills not available", "hook_code": "// Dummy useChatKit hook code"}
    async def create_chatkit_session(*args, **kwargs):
        return {"success": False, "error": "Skills not available", "session_data": {"session_id": "dummy-id", "client_secret": "dummy-secret"}}
    async def generate_chatkit_integration_code(*args, **kwargs):
        return {"success": False, "error": "Skills not available", "integration_code": "// Dummy integration code"}
    async def write_chatkit_component_to_file(*args, **kwargs):
        return {"success": False, "error": "Skills not available"}


class OpenAIChatKitFrontendSubagent:
    """
    OpenAI ChatKit Frontend Subagent - Specializes in creating and managing OpenAI ChatKit frontend components.
    """
    def __init__(self):
        self.subagent_id = str(uuid.uuid4())
        self.name = "openai_chatkit_frontend_subagent"
        self.description = "OpenAI ChatKit Frontend Manager - Creates and manages OpenAI ChatKit frontend components"
        self.capabilities = [
            "create-chatkit-ui-component",
            "create-chatkit-hook",
            "create-chatkit-session",
            "generate-integration-code",
            "write-component-to-file",
            "manage-frontend-components"
        ]
        self.components_registry: Dict[str, Dict[str, Any]] = {}
        self.sessions_registry: Dict[str, Dict[str, Any]] = {}

    async def create_ui_component(self, component_name: str, props: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a ChatKit UI component."""
        try:
            result = await create_chatkit_ui_component(component_name, props)

            if result.get("success"):
                component_id = str(uuid.uuid4())

                # Register the component in our internal registry
                self.components_registry[component_id] = {
                    "id": component_id,
                    "name": component_name,
                    "code": result["component_code"],
                    "props": props or {},
                    "created_at": datetime.utcnow().isoformat(),
                    "type": "ui_component"
                }

                logger.info(f"Created UI component '{component_name}' with ID: {component_id}")

                return {
                    "success": True,
                    "component_id": component_id,
                    "component_code": result["component_code"],
                    "message": f"UI component '{component_name}' created successfully with ID {component_id}"
                }
            else:
                return result

        except Exception as e:
            logger.error(f"Failed to create UI component: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    async def create_hook(self, hook_name: str, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a ChatKit hook."""
        try:
            result = await create_chatkit_hook(hook_name, config)

            if result.get("success"):
                hook_id = str(uuid.uuid4())

                # Register the hook in our internal registry
                self.components_registry[hook_id] = {
                    "id": hook_id,
                    "name": hook_name,
                    "code": result["hook_code"],
                    "config": config or {},
                    "created_at": datetime.utcnow().isoformat(),
                    "type": "hook"
                }

                logger.info(f"Created hook '{hook_name}' with ID: {hook_id}")

                return {
                    "success": True,
                    "hook_id": hook_id,
                    "hook_code": result["hook_code"],
                    "message": f"Hook '{hook_name}' created successfully with ID {hook_id}"
                }
            else:
                return result

        except Exception as e:
            logger.error(f"Failed to create hook: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    async def create_session(self, workflow_id: str, user_id: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a ChatKit session."""
        try:
            result = await create_chatkit_session(workflow_id, user_id, metadata)

            if result.get("success"):
                session_data = result["session_data"]
                session_id = session_data["session_id"]

                # Register the session in our internal registry
                self.sessions_registry[session_id] = {
                    "id": session_id,
                    "workflow_id": workflow_id,
                    "user_id": user_id,
                    "session_data": session_data,
                    "created_at": datetime.utcnow().isoformat(),
                    "type": "session"
                }

                logger.info(f"Created session '{session_id}' for user '{user_id}'")

                return {
                    "success": True,
                    "session_data": session_data,
                    "message": f"Session created successfully with ID {session_id}"
                }
            else:
                return result

        except Exception as e:
            logger.error(f"Failed to create session: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    async def generate_integration(self, integration_type: str, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate integration code."""
        try:
            result = await generate_chatkit_integration_code(integration_type, config)

            if result.get("success"):
                integration_id = str(uuid.uuid4())

                # Register the integration in our internal registry
                self.components_registry[integration_id] = {
                    "id": integration_id,
                    "type_name": integration_type,
                    "code": result["integration_code"],
                    "config": config or {},
                    "created_at": datetime.utcnow().isoformat(),
                    "type": "integration"
                }

                logger.info(f"Generated integration code for '{integration_type}' with ID: {integration_id}")

                return {
                    "success": True,
                    "integration_id": integration_id,
                    "integration_code": result["integration_code"],
                    "message": f"Integration code for '{integration_type}' generated successfully with ID {integration_id}"
                }
            else:
                return result

        except Exception as e:
            logger.error(f"Failed to generate integration code: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    async def write_component_to_file(self, component_name: str, file_path: str, props: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Write a component to a file."""
        try:
            # Determine if this is a hook or component based on the name
            if "hook" in component_name.lower() or component_name.lower().startswith("use"):
                # Use the hook creation function for hooks
                result = await create_chatkit_hook(component_name, props)
                if result.get("success"):
                    # Write the hook code to the file
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(result["hook_code"])
            else:
                # Use the component creation function for components
                result = await write_chatkit_component_to_file(component_name, file_path, props)

            if result.get("success"):
                file_write_id = str(uuid.uuid4())

                return {
                    "success": True,
                    "file_path": file_path,
                    "message": f"Component '{component_name}' written to {file_path}"
                }
            else:
                return result

        except Exception as e:
            logger.error(f"Failed to write component to file: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    async def get_component_info(self, component_id: str) -> Dict[str, Any]:
        """Get information about a specific component."""
        try:
            if component_id not in self.components_registry:
                return {
                    "success": False,
                    "error": f"Component with ID '{component_id}' not found in registry"
                }

            component_info = self.components_registry[component_id]

            return {
                "success": True,
                "component_info": component_info
            }

        except Exception as e:
            logger.error(f"Failed to get component info: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    async def list_components(self) -> Dict[str, Any]:
        """List all registered components."""
        try:
            components_list = []
            for comp_id, comp_data in self.components_registry.items():
                components_list.append({
                    "id": comp_id,
                    "name": comp_data.get("name", comp_data.get("type_name", "unknown")),
                    "type": comp_data["type"],
                    "created_at": comp_data["created_at"]
                })

            return {
                "success": True,
                "components_count": len(components_list),
                "components": components_list
            }

        except Exception as e:
            logger.error(f"Failed to list components: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    async def get_session_info(self, session_id: str) -> Dict[str, Any]:
        """Get information about a specific session."""
        try:
            if session_id not in self.sessions_registry:
                return {
                    "success": False,
                    "error": f"Session with ID '{session_id}' not found in registry"
                }

            session_info = self.sessions_registry[session_id]

            return {
                "success": True,
                "session_info": session_info
            }

        except Exception as e:
            logger.error(f"Failed to get session info: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    async def list_sessions(self) -> Dict[str, Any]:
        """List all registered sessions."""
        try:
            sessions_list = []
            for sess_id, sess_data in self.sessions_registry.items():
                sessions_list.append({
                    "id": sess_id,
                    "workflow_id": sess_data["workflow_id"],
                    "user_id": sess_data["user_id"],
                    "created_at": sess_data["created_at"]
                })

            return {
                "success": True,
                "sessions_count": len(sessions_list),
                "sessions": sessions_list
            }

        except Exception as e:
            logger.error(f"Failed to list sessions: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    async def handle_task(self, task_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming tasks for the OpenAI ChatKit Frontend subagent."""
        try:
            if task_name == "create_ui_component":
                component_name = arguments.get("component_name")
                props = arguments.get("props", {})

                if not component_name:
                    return {
                        "success": False,
                        "error": "'component_name' is required"
                    }

                return await self.create_ui_component(component_name, props)

            elif task_name == "create_hook":
                hook_name = arguments.get("hook_name")
                config = arguments.get("config", {})

                if not hook_name:
                    return {
                        "success": False,
                        "error": "'hook_name' is required"
                    }

                return await self.create_hook(hook_name, config)

            elif task_name == "create_session":
                workflow_id = arguments.get("workflow_id")
                user_id = arguments.get("user_id")
                metadata = arguments.get("metadata", {})

                if not workflow_id or not user_id:
                    return {
                        "success": False,
                        "error": "Both 'workflow_id' and 'user_id' are required"
                    }

                return await self.create_session(workflow_id, user_id, metadata)

            elif task_name == "generate_integration":
                integration_type = arguments.get("integration_type")
                config = arguments.get("config", {})

                if not integration_type:
                    return {
                        "success": False,
                        "error": "'integration_type' is required"
                    }

                return await self.generate_integration(integration_type, config)

            elif task_name == "write_component_to_file":
                component_name = arguments.get("component_name")
                file_path = arguments.get("file_path")
                props = arguments.get("props", {})

                if not component_name or not file_path:
                    return {
                        "success": False,
                        "error": "Both 'component_name' and 'file_path' are required"
                    }

                return await self.write_component_to_file(component_name, file_path, props)

            elif task_name == "get_component_info":
                component_id = arguments.get("component_id")

                if not component_id:
                    return {
                        "success": False,
                        "error": "'component_id' is required"
                    }

                return await self.get_component_info(component_id)

            elif task_name == "list_components":
                return await self.list_components()

            elif task_name == "get_session_info":
                session_id = arguments.get("session_id")

                if not session_id:
                    return {
                        "success": False,
                        "error": "'session_id' is required"
                    }

                return await self.get_session_info(session_id)

            elif task_name == "list_sessions":
                return await self.list_sessions()

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


async def run_openai_chatkit_frontend_subagent():
    """
    Run the OpenAI ChatKit Frontend Subagent as a standalone component
    """
    print("Initializing OpenAI ChatKit Frontend Subagent...")
    print("=" * 60)

    # Create the subagent instance
    subagent = OpenAIChatKitFrontendSubagent()

    print("+ OpenAI ChatKit Frontend Subagent initialized successfully!")
    print(f"  - Subagent ID: {subagent.subagent_id}")
    print(f"  - Subagent Name: {subagent.name}")
    print(f"  - Description: {subagent.description}")
    print(f"  - Capabilities: {len(subagent.capabilities)}")
    for cap in subagent.capabilities:
        print(f"    * {cap}")

    # Demonstrate the subagent functionality
    print("\nDemonstrating subagent functionality:")

    # Create a ChatKit UI component
    ui_component_result = await subagent.create_ui_component(
        component_name="ChatKitUI",
        props={"sessionId": None, "workflowId": None, "userId": None}
    )
    if ui_component_result["success"]:
        ui_component_id = ui_component_result["component_id"]
        print(f"  + Created ChatKitUI component: {ui_component_id[:8]}...")
    else:
        print(f"  X Failed to create ChatKitUI component: {ui_component_result['error']}")

    # Create a useChatKit hook
    hook_result = await subagent.create_hook(
        hook_name="useChatKit",
        config={"autoConnect": True, "reconnectAttempts": 3}
    )
    if hook_result["success"]:
        hook_id = hook_result["hook_id"]
        print(f"  + Created useChatKit hook: {hook_id[:8]}...")
    else:
        print(f"  X Failed to create useChatKit hook: {hook_result['error']}")

    # Create a ChatKit session
    session_result = await subagent.create_session(
        workflow_id="support-workflow",
        user_id="user-123",
        metadata={"department": "support", "priority": "high"}
    )
    if session_result["success"]:
        session_id = session_result["session_data"]["session_id"]
        print(f"  + Created ChatKit session: {session_id[:8]}...")
    else:
        print(f"  X Failed to create ChatKit session: {session_result['error']}")

    # Generate integration code
    integration_result = await subagent.generate_integration(
        integration_type="component",
        config={}
    )
    if integration_result["success"]:
        integration_id = integration_result["integration_id"]
        print(f"  + Generated integration code: {integration_id[:8]}...")
    else:
        print(f"  X Failed to generate integration code: {integration_result['error']}")

    # List all created components
    components_list = await subagent.list_components()
    if components_list["success"]:
        print(f"\n  + Total components created: {components_list['components_count']}")
        for comp in components_list["components"]:
            print(f"    - {comp['name']} ({comp['type']}): {comp['id'][:8]}...")

    # List all created sessions
    sessions_list = await subagent.list_sessions()
    if sessions_list["success"]:
        print(f"  + Total sessions created: {sessions_list['sessions_count']}")
        for sess in sessions_list["sessions"]:
            print(f"    - Workflow {sess['workflow_id']} for user {sess['user_id']}: {sess['id'][:8]}...")

    print("\n+ OpenAI ChatKit Frontend Subagent is ready to handle requests!")
    print("Use the subagent instance to call create_ui_component(), create_hook(), or handle_task() methods.")

    return subagent


if __name__ == "__main__":
    try:
        subagent = asyncio.run(run_openai_chatkit_frontend_subagent())
        print("\nSubagent is running and ready to handle requests!")
    except Exception as e:
        print(f"\nX Error running OpenAI ChatKit Frontend Subagent: {e}")
        import traceback
        traceback.print_exc()