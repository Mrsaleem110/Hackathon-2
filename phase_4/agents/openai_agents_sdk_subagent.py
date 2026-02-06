#!/usr/bin/env python3
"""
OpenAI Agents SDK Subagent
This subagent specializes in creating and managing OpenAI agents using the OpenAI Agents SDK.
"""
import asyncio
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import the OpenAI Agents SDK skills
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))  # Add parent directory to path

try:
    from skills.openai_agents_sdk.openai_agent_skills import (
        create_openai_agent,
        create_openai_handoff_agent,
        create_openai_guardrail_agent,
        run_openai_agent_orchestration,
        add_guardrail_to_openai_agent,
        create_homework_guardrail,
        create_complex_agent_orchestration
    )
except ImportError as e:
    logger.warning(f"OpenAI Agents SDK skills not available: {e}. Please install the skills first.")
    # Define dummy functions for testing
    async def create_openai_agent(*args, **kwargs):
        return {"success": False, "error": "Skills not available", "agent_config": {"name": kwargs.get("name", "dummy"), "instructions": kwargs.get("instructions", ""), "model": kwargs.get("model", "gpt-4")}}
    async def create_openai_handoff_agent(*args, **kwargs):
        return {"success": False, "error": "Skills not available", "agent_config": {"name": kwargs.get("name", "dummy"), "instructions": kwargs.get("instructions", ""), "model": kwargs.get("model", "gpt-4"), "handoffs": kwargs.get("handoff_targets", [])}}
    async def create_openai_guardrail_agent(*args, **kwargs):
        return {"success": False, "error": "Skills not available", "agent_config": {"name": kwargs.get("name", "dummy"), "instructions": kwargs.get("instructions", ""), "model": kwargs.get("model", "gpt-4"), "is_guardrail": True}}
    async def run_openai_agent_orchestration(*args, **kwargs):
        return {"success": False, "error": "Skills not available"}
    async def add_guardrail_to_openai_agent(*args, **kwargs):
        return {"success": False, "error": "Skills not available"}
    async def create_homework_guardrail(*args, **kwargs):
        return {"success": False, "error": "Skills not available"}
    async def create_complex_agent_orchestration(*args, **kwargs):
        return {"success": False, "error": "Skills not available"}


class OpenAIAgentsSDKSubagent:
    """
    OpenAI Agents SDK Subagent - Specializes in creating and managing OpenAI agents using the OpenAI Agents SDK.
    """
    def __init__(self):
        self.subagent_id = str(uuid.uuid4())
        self.name = "openai_agents_sdk_subagent"
        self.description = "OpenAI Agents SDK Manager - Creates and manages OpenAI agents using the OpenAI Agents SDK"
        self.capabilities = [
            "create-agent",
            "create-handoff-agent",
            "create-guardrail-agent",
            "run-agent-orchestration",
            "add-guardrail-to-agent",
            "create-homework-guardrail",
            "create-complex-orchestration",
            "manage-agents"
        ]
        self.agents_registry: Dict[str, Dict[str, Any]] = {}

    async def create_agent(self, name: str, instructions: str, model: Optional[str] = None,
                          handoff_description: Optional[str] = None) -> Dict[str, Any]:
        """Create a new OpenAI agent."""
        try:
            result = await create_openai_agent(
                name=name,
                instructions=instructions,
                model=model,
                handoff_description=handoff_description
            )

            if result.get("success"):
                agent_config = result["agent_config"]
                agent_id = str(uuid.uuid4())

                # Register the agent in our internal registry
                self.agents_registry[agent_id] = {
                    "id": agent_id,
                    "config": agent_config,
                    "created_at": datetime.utcnow().isoformat(),
                    "type": "basic"
                }

                logger.info(f"Created agent '{name}' with ID: {agent_id}")

                return {
                    "success": True,
                    "agent_id": agent_id,
                    "agent_config": agent_config,
                    "message": f"Agent '{name}' created successfully with ID {agent_id}"
                }
            else:
                return result

        except Exception as e:
            logger.error(f"Failed to create agent: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    async def create_handoff_agent(self, name: str, instructions: str,
                                 handoff_targets: List[Dict[str, Any]],
                                 model: Optional[str] = None) -> Dict[str, Any]:
        """Create an agent with handoff capabilities."""
        try:
            result = await create_openai_handoff_agent(
                name=name,
                instructions=instructions,
                handoff_targets=handoff_targets,
                model=model
            )

            if result.get("success"):
                agent_config = result["agent_config"]
                agent_id = str(uuid.uuid4())

                # Register the agent in our internal registry
                self.agents_registry[agent_id] = {
                    "id": agent_id,
                    "config": agent_config,
                    "created_at": datetime.utcnow().isoformat(),
                    "type": "handoff"
                }

                logger.info(f"Created handoff agent '{name}' with ID: {agent_id}")

                return {
                    "success": True,
                    "agent_id": agent_id,
                    "agent_config": agent_config,
                    "message": f"Handoff agent '{name}' created successfully with ID {agent_id}"
                }
            else:
                return result

        except Exception as e:
            logger.error(f"Failed to create handoff agent: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    async def create_guardrail_agent(self, name: str, instructions: str,
                                  output_type: Optional[str] = None,
                                  model: Optional[str] = None) -> Dict[str, Any]:
        """Create an agent with guardrail functionality."""
        try:
            result = await create_openai_guardrail_agent(
                name=name,
                instructions=instructions,
                output_type=output_type,
                model=model
            )

            if result.get("success"):
                agent_config = result["agent_config"]
                agent_id = str(uuid.uuid4())

                # Register the agent in our internal registry
                self.agents_registry[agent_id] = {
                    "id": agent_id,
                    "config": agent_config,
                    "created_at": datetime.utcnow().isoformat(),
                    "type": "guardrail"
                }

                logger.info(f"Created guardrail agent '{name}' with ID: {agent_id}")

                return {
                    "success": True,
                    "agent_id": agent_id,
                    "agent_config": agent_config,
                    "message": f"Guardrail agent '{name}' created successfully with ID {agent_id}"
                }
            else:
                return result

        except Exception as e:
            logger.error(f"Failed to create guardrail agent: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    async def run_orchestration(self, agent_id: str, user_input: str,
                              max_steps: Optional[int] = 10) -> Dict[str, Any]:
        """Run an agent orchestration with the specified agent."""
        try:
            if agent_id not in self.agents_registry:
                return {
                    "success": False,
                    "error": f"Agent with ID '{agent_id}' not found in registry"
                }

            agent_config = self.agents_registry[agent_id]["config"]

            result = await run_openai_agent_orchestration(
                initial_agent=agent_config,
                user_input=user_input,
                max_steps=max_steps
            )

            return result

        except Exception as e:
            logger.error(f"Failed to run orchestration: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    async def add_guardrail_to_agent(self, agent_id: str, guardrail_func_name: str) -> Dict[str, Any]:
        """Add a guardrail to an existing agent."""
        try:
            if agent_id not in self.agents_registry:
                return {
                    "success": False,
                    "error": f"Agent with ID '{agent_id}' not found in registry"
                }

            agent_config = self.agents_registry[agent_id]["config"]

            result = await add_guardrail_to_openai_agent(
                agent_config=agent_config,
                guardrail_func_name=guardrail_func_name
            )

            if result.get("success"):
                # Update the agent config in our registry
                self.agents_registry[agent_id]["config"] = result["updated_agent_config"]

                return {
                    "success": True,
                    "agent_id": agent_id,
                    "updated_agent_config": result["updated_agent_config"],
                    "message": f"Guardrail '{guardrail_func_name}' added to agent '{agent_id}'"
                }
            else:
                return result

        except Exception as e:
            logger.error(f"Failed to add guardrail to agent: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    async def create_homework_guardrail_for_agent(self, agent_id: str) -> Dict[str, Any]:
        """Add a homework guardrail to an existing agent."""
        try:
            if agent_id not in self.agents_registry:
                return {
                    "success": False,
                    "error": f"Agent with ID '{agent_id}' not found in registry"
                }

            agent_config = self.agents_registry[agent_id]["config"]

            result = await create_homework_guardrail(
                agent_config=agent_config
            )

            if result.get("success"):
                # Update the agent config in our registry
                self.agents_registry[agent_id]["config"] = result["updated_agent_config"]

                return {
                    "success": True,
                    "agent_id": agent_id,
                    "updated_agent_config": result["updated_agent_config"],
                    "message": f"Homework guardrail added to agent '{agent_id}'"
                }
            else:
                return result

        except Exception as e:
            logger.error(f"Failed to add homework guardrail to agent: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    async def get_agent_info(self, agent_id: str) -> Dict[str, Any]:
        """Get information about a specific agent."""
        try:
            if agent_id not in self.agents_registry:
                return {
                    "success": False,
                    "error": f"Agent with ID '{agent_id}' not found in registry"
                }

            agent_info = self.agents_registry[agent_id]

            return {
                "success": True,
                "agent_info": agent_info
            }

        except Exception as e:
            logger.error(f"Failed to get agent info: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    async def list_agents(self) -> Dict[str, Any]:
        """List all registered agents."""
        try:
            agents_list = []
            for agent_id, agent_data in self.agents_registry.items():
                agents_list.append({
                    "id": agent_id,
                    "name": agent_data["config"]["name"],
                    "type": agent_data["type"],
                    "created_at": agent_data["created_at"]
                })

            return {
                "success": True,
                "agents_count": len(agents_list),
                "agents": agents_list
            }

        except Exception as e:
            logger.error(f"Failed to list agents: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    async def handle_task(self, task_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming tasks for the OpenAI Agents SDK subagent."""
        try:
            if task_name == "create_agent":
                name = arguments.get("name")
                instructions = arguments.get("instructions")
                model = arguments.get("model")
                handoff_description = arguments.get("handoff_description")

                if not name or not instructions:
                    return {
                        "success": False,
                        "error": "Both 'name' and 'instructions' are required"
                    }

                return await self.create_agent(name, instructions, model, handoff_description)

            elif task_name == "create_handoff_agent":
                name = arguments.get("name")
                instructions = arguments.get("instructions")
                handoff_targets = arguments.get("handoff_targets", [])
                model = arguments.get("model")

                if not name or not instructions:
                    return {
                        "success": False,
                        "error": "Both 'name' and 'instructions' are required"
                    }

                return await self.create_handoff_agent(name, instructions, handoff_targets, model)

            elif task_name == "create_guardrail_agent":
                name = arguments.get("name")
                instructions = arguments.get("instructions")
                output_type = arguments.get("output_type")
                model = arguments.get("model")

                if not name or not instructions:
                    return {
                        "success": False,
                        "error": "Both 'name' and 'instructions' are required"
                    }

                return await self.create_guardrail_agent(name, instructions, output_type, model)

            elif task_name == "run_orchestration":
                agent_id = arguments.get("agent_id")
                user_input = arguments.get("user_input")
                max_steps = arguments.get("max_steps", 10)

                if not agent_id or not user_input:
                    return {
                        "success": False,
                        "error": "Both 'agent_id' and 'user_input' are required"
                    }

                return await self.run_orchestration(agent_id, user_input, max_steps)

            elif task_name == "add_guardrail_to_agent":
                agent_id = arguments.get("agent_id")
                guardrail_func_name = arguments.get("guardrail_func_name")

                if not agent_id or not guardrail_func_name:
                    return {
                        "success": False,
                        "error": "Both 'agent_id' and 'guardrail_func_name' are required"
                    }

                return await self.add_guardrail_to_agent(agent_id, guardrail_func_name)

            elif task_name == "create_homework_guardrail_for_agent":
                agent_id = arguments.get("agent_id")

                if not agent_id:
                    return {
                        "success": False,
                        "error": "'agent_id' is required"
                    }

                return await self.create_homework_guardrail_for_agent(agent_id)

            elif task_name == "get_agent_info":
                agent_id = arguments.get("agent_id")

                if not agent_id:
                    return {
                        "success": False,
                        "error": "'agent_id' is required"
                    }

                return await self.get_agent_info(agent_id)

            elif task_name == "list_agents":
                return await self.list_agents()

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


async def run_openai_agents_sdk_subagent():
    """
    Run the OpenAI Agents SDK Subagent as a standalone component
    """
    print("Initializing OpenAI Agents SDK Subagent...")
    print("=" * 60)

    # Create the subagent instance
    subagent = OpenAIAgentsSDKSubagent()

    print("+ OpenAI Agents SDK Subagent initialized successfully!")
    print(f"  - Subagent ID: {subagent.subagent_id}")
    print(f"  - Subagent Name: {subagent.name}")
    print(f"  - Description: {subagent.description}")
    print(f"  - Capabilities: {len(subagent.capabilities)}")
    for cap in subagent.capabilities:
        print(f"    * {cap}")

    # Demonstrate the subagent functionality
    print("\nDemonstrating subagent functionality:")

    # Create a math tutor agent
    math_agent_result = await subagent.create_agent(
        name="Math Tutor",
        instructions="You provide help with math problems. Explain your reasoning at each step and include examples",
        model="gpt-4"
    )
    if math_agent_result["success"]:
        math_agent_id = math_agent_result["agent_id"]
        print(f"  + Created Math Tutor agent: {math_agent_id[:8]}...")
    else:
        print(f"  X Failed to create Math Tutor agent: {math_agent_result['error']}")

    # Create a history tutor agent
    history_agent_result = await subagent.create_agent(
        name="History Tutor",
        instructions="You provide assistance with historical queries. Explain important events and context clearly.",
        handoff_description="Specialist agent for historical questions"
    )
    if history_agent_result["success"]:
        history_agent_id = history_agent_result["agent_id"]
        print(f"  + Created History Tutor agent: {history_agent_id[:8]}...")
    else:
        print(f"  X Failed to create History Tutor agent: {history_agent_result['error']}")

    # Create a triage agent with handoff capabilities
    if 'math_agent_id' in locals() and 'history_agent_id' in locals():
        triage_result = await subagent.create_handoff_agent(
            name="Triage Agent",
            instructions="You determine which agent to use based on the user's homework question",
            handoff_targets=[
                {
                    "name": "History Tutor",
                    "handoff_description": "Specialist agent for historical questions"
                },
                {
                    "name": "Math Tutor",
                    "handoff_description": "Specialist agent for math questions"
                }
            ]
        )
        if triage_result["success"]:
            triage_agent_id = triage_result["agent_id"]
            print(f"  + Created Triage agent with handoffs: {triage_agent_id[:8]}...")
        else:
            print(f"  X Failed to create Triage agent: {triage_result['error']}")

    # List all created agents
    agents_list = await subagent.list_agents()
    if agents_list["success"]:
        print(f"\n  + Total agents created: {agents_list['agents_count']}")
        for agent in agents_list["agents"]:
            print(f"    - {agent['name']} ({agent['type']}): {agent['id'][:8]}...")

    print("\n+ OpenAI Agents SDK Subagent is ready to handle requests!")
    print("Use the subagent instance to call create_agent(), create_handoff_agent(), or handle_task() methods.")

    return subagent


if __name__ == "__main__":
    try:
        subagent = asyncio.run(run_openai_agents_sdk_subagent())
        print("\nSubagent is running and ready to handle requests!")
    except Exception as e:
        print(f"\nX Error running OpenAI Agents SDK Subagent: {e}")
        import traceback
        traceback.print_exc()