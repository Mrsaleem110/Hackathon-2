"""
OpenAI Agents SDK Skills
This module provides skills for creating and managing OpenAI agents using the OpenAI Agents SDK.
"""
import asyncio
import json
from typing import Dict, Any, Optional, List
from pydantic import BaseModel


class HomeworkOutput(BaseModel):
    """Pydantic model for homework guardrail output."""
    is_homework: bool
    reasoning: str


class OpenAIAgentSkills:
    """
    Skills for working with the OpenAI Agents SDK.
    These skills provide high-level operations for creating and managing agents.
    """

    def __init__(self):
        self.skill_name = "openai_agents_sdk_skills"
        self.description = "Skills for creating and managing OpenAI agents using the OpenAI Agents SDK"

    async def create_agent(self, name: str, instructions: str, model: Optional[str] = None,
                          handoff_description: Optional[str] = None, tools: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Create a new OpenAI agent with the specified parameters.

        Args:
            name: Name of the agent
            instructions: Instructions for the agent's behavior
            model: Model to use for the agent (optional, defaults to gpt-4)
            handoff_description: Description for handoff scenarios (optional)
            tools: List of tools available to the agent (optional)

        Returns:
            Dictionary containing agent configuration or error information
        """
        try:
            # Validate required parameters
            if not name or not instructions:
                return {
                    "error": "Both 'name' and 'instructions' are required parameters"
                }

            # Set default model if not provided
            if model is None:
                model = "gpt-4"

            # Create the agent configuration
            agent_config = {
                "name": name,
                "instructions": instructions,
                "model": model,
                "handoff_description": handoff_description,
                "tools": tools or [],
                "created_at": asyncio.get_event_loop().time()
            }

            # In a real implementation, this would create the agent using the OpenAI Agents SDK
            # For this implementation, we'll return the configuration as if the agent was created
            return {
                "success": True,
                "agent_config": agent_config,
                "message": f"Agent '{name}' configured successfully"
            }

        except Exception as e:
            return {"error": f"Failed to create agent: {str(e)}"}

    async def create_handoff_agent(self, name: str, instructions: str, handoff_targets: List[Dict[str, Any]],
                                  model: Optional[str] = None) -> Dict[str, Any]:
        """
        Create an agent that can handoff to other agents.

        Args:
            name: Name of the agent
            instructions: Instructions for the agent's behavior
            handoff_targets: List of agent configurations that this agent can handoff to
            model: Model to use for the agent (optional, defaults to gpt-4)

        Returns:
            Dictionary containing agent configuration with handoff capabilities or error information
        """
        try:
            # Validate required parameters
            if not name or not instructions:
                return {
                    "error": "Both 'name' and 'instructions' are required parameters"
                }

            if not handoff_targets or not isinstance(handoff_targets, list):
                return {
                    "error": "'handoff_targets' must be a non-empty list of agent configurations"
                }

            # Validate that each handoff target has required fields
            for i, target in enumerate(handoff_targets):
                if not isinstance(target, dict):
                    return {"error": f"Handoff target at index {i} is not a dictionary"}
                if "name" not in target or "handoff_description" not in target:
                    return {"error": f"Handoff target at index {i} must have 'name' and 'handoff_description'"}

            # Set default model if not provided
            if model is None:
                model = "gpt-4"

            # Create the handoff agent configuration
            agent_config = {
                "name": name,
                "instructions": instructions,
                "model": model,
                "handoffs": handoff_targets,
                "created_at": asyncio.get_event_loop().time()
            }

            return {
                "success": True,
                "agent_config": agent_config,
                "message": f"Handoff agent '{name}' configured successfully with {len(handoff_targets)} handoff targets"
            }

        except Exception as e:
            return {"error": f"Failed to create handoff agent: {str(e)}"}

    async def create_guardrail_agent(self, name: str, instructions: str, output_type: Optional[str] = None,
                                   model: Optional[str] = None) -> Dict[str, Any]:
        """
        Create an agent that implements input/output guardrails.

        Args:
            name: Name of the agent
            instructions: Instructions for the agent's behavior
            output_type: Expected output type for validation (optional)
            model: Model to use for the agent (optional, defaults to gpt-4)

        Returns:
            Dictionary containing guardrail agent configuration or error information
        """
        try:
            # Validate required parameters
            if not name or not instructions:
                return {
                    "error": "Both 'name' and 'instructions' are required parameters"
                }

            # Set default model if not provided
            if model is None:
                model = "gpt-4"

            # Create the guardrail agent configuration
            agent_config = {
                "name": name,
                "instructions": instructions,
                "model": model,
                "output_type": output_type,
                "is_guardrail": True,
                "created_at": asyncio.get_event_loop().time()
            }

            return {
                "success": True,
                "agent_config": agent_config,
                "message": f"Guardrail agent '{name}' configured successfully"
            }

        except Exception as e:
            return {"error": f"Failed to create guardrail agent: {str(e)}"}

    async def run_agent_orchestration(self, initial_agent: Dict[str, Any],
                                     user_input: str, max_steps: Optional[int] = 10) -> Dict[str, Any]:
        """
        Run an agent orchestration with potential handoffs and guardrails.

        Args:
            initial_agent: Configuration of the initial agent to start with
            user_input: Input from the user to process
            max_steps: Maximum number of steps to execute (prevents infinite loops)

        Returns:
            Dictionary containing the final result of the orchestration or error information
        """
        try:
            # Validate required parameters
            if not initial_agent or not user_input:
                return {
                    "error": "Both 'initial_agent' and 'user_input' are required parameters"
                }

            # Check for input guardrails and apply them
            input_guardrails = initial_agent.get("input_guardrails", [])
            for guardrail in input_guardrails:
                # Simulate guardrail check - in a real implementation, this would call the guardrail function
                if guardrail.get("function_name") == "homework_guardrail":
                    # Simulate homework guardrail check
                    is_homework = any(keyword in user_input.lower() for keyword in ["homework", "math", "calculate", "problem", "question"])
                    if not is_homework:
                        return {
                            "success": False,
                            "error": "Input guardrail triggered: Content does not appear to be homework-related",
                            "guardrail_name": "homework_guardrail",
                            "execution_trace": [{
                                "step": 1,
                                "action": "input_guardrail_check",
                                "guardrail": "homework_guardrail",
                                "input": user_input,
                                "result": "blocked",
                                "reason": "Not homework-related content",
                                "timestamp": asyncio.get_event_loop().time()
                            }]
                        }

            # Simulate the agent orchestration process
            # In a real implementation, this would use the OpenAI Agents SDK to run the agents
            result = {
                "initial_agent": initial_agent.get("name", "unknown"),
                "input": user_input,
                "steps_executed": 0,
                "final_output": "",
                "handoff_occurred": False,
                "handoff_to": None,
                "execution_trace": []
            }

            # Add guardrail check step to trace
            if input_guardrails:
                result["execution_trace"].append({
                    "step": 1,
                    "action": "input_guardrail_check",
                    "guardrails_applied": len(input_guardrails),
                    "result": "passed",
                    "timestamp": asyncio.get_event_loop().time()
                })

            # Simulate processing steps
            current_agent = initial_agent
            for step in range(max_steps):
                step_num = len(result["execution_trace"]) + 1
                step_info = {
                    "step": step_num,
                    "agent": current_agent.get("name", f"step-{step+1}"),
                    "action": "processing",
                    "input": user_input if step == 0 else f"Continuing from step {step}",
                    "timestamp": asyncio.get_event_loop().time()
                }

                # Add step to execution trace
                result["execution_trace"].append(step_info)

                # Check for handoff opportunities
                if "handoffs" in current_agent and len(current_agent["handoffs"]) > 0:
                    # Determine if a handoff should occur based on the user input
                    handoff_keywords = ["math", "calculate", "history", "science", "learn"]
                    should_handoff = any(keyword in user_input.lower() for keyword in handoff_keywords)

                    if should_handoff:
                        # Find the most appropriate handoff target based on keywords
                        target_agent = None
                        for handoff in current_agent["handoffs"]:
                            if any(keyword in handoff.get("handoff_description", "").lower() for keyword in handoff_keywords):
                                target_agent = handoff
                                break

                        # If no specific match, use the first available handoff
                        if not target_agent:
                            target_agent = current_agent["handoffs"][0]

                        result["handoff_occurred"] = True
                        result["handoff_to"] = target_agent.get("name", "unknown")
                        current_agent = target_agent

                        # Add handoff step to trace
                        handoff_step = {
                            "step": len(result["execution_trace"]) + 1,
                            "agent": initial_agent.get("name", "unknown"),
                            "action": "handoff_decision",
                            "handoff_to": target_agent.get("name", "unknown"),
                            "reason": f"Detected topic matching handoff criteria: {', '.join([k for k in handoff_keywords if k in user_input.lower()])}",
                            "timestamp": asyncio.get_event_loop().time()
                        }
                        result["execution_trace"].append(handoff_step)

                # Simulate processing and generate output
                if step == max_steps - 1 or (step > 0 and result["handoff_occurred"]):
                    # Final step or after handoff decision
                    result["final_output"] = f"Processed input: '{user_input}' with agent '{current_agent.get('name', 'unknown')}'"
                    result["steps_executed"] = len(result["execution_trace"])
                    break

            return {
                "success": True,
                "result": result,
                "message": f"Agent orchestration completed after {result['steps_executed']} steps"
            }

        except Exception as e:
            return {"error": f"Failed to run agent orchestration: {str(e)}"}

    async def add_guardrail_to_agent(self, agent_config: Dict[str, Any], guardrail_func_name: str) -> Dict[str, Any]:
        """
        Add a guardrail function to an existing agent configuration.

        Args:
            agent_config: Existing agent configuration to add guardrail to
            guardrail_func_name: Name of the guardrail function to add

        Returns:
            Dictionary containing updated agent configuration or error information
        """
        try:
            if not agent_config or not guardrail_func_name:
                return {
                    "error": "Both 'agent_config' and 'guardrail_func_name' are required parameters"
                }

            # Add the guardrail to the agent configuration
            updated_config = agent_config.copy()

            if "input_guardrails" not in updated_config:
                updated_config["input_guardrails"] = []

            updated_config["input_guardrails"].append({
                "function_name": guardrail_func_name,
                "added_at": asyncio.get_event_loop().time()
            })

            return {
                "success": True,
                "updated_agent_config": updated_config,
                "message": f"Guardrail '{guardrail_func_name}' added to agent '{updated_config.get('name', 'unknown')}'"
            }

        except Exception as e:
            return {"error": f"Failed to add guardrail to agent: {str(e)}"}

    async def create_homework_guardrail(self, agent_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create and add a homework-specific guardrail to an agent.

        Args:
            agent_config: Agent configuration to add the homework guardrail to

        Returns:
            Dictionary containing updated agent configuration with homework guardrail
        """
        try:
            if not agent_config:
                return {
                    "error": "'agent_config' is required"
                }

            # Add the homework guardrail to the agent configuration
            updated_config = agent_config.copy()

            if "input_guardrails" not in updated_config:
                updated_config["input_guardrails"] = []

            # Add the homework guardrail
            homework_guardrail = {
                "function_name": "homework_guardrail",
                "description": "Check if the user is asking about homework",
                "type": "input_guardrail",
                "added_at": asyncio.get_event_loop().time()
            }

            updated_config["input_guardrails"].append(homework_guardrail)

            return {
                "success": True,
                "updated_agent_config": updated_config,
                "message": f"Homework guardrail added to agent '{updated_config.get('name', 'unknown')}'"
            }

        except Exception as e:
            return {"error": f"Failed to add homework guardrail to agent: {str(e)}"}

    async def create_complex_agent_orchestration(self, agents: List[Dict[str, Any]],
                                               user_input: str,
                                               max_steps: Optional[int] = 10) -> Dict[str, Any]:
        """
        Run a complex agent orchestration with multiple agents, handoffs, and guardrails.

        Args:
            agents: List of agent configurations
            user_input: Input from the user to process
            max_steps: Maximum number of steps to execute (prevents infinite loops)

        Returns:
            Dictionary containing the final result of the complex orchestration or error information
        """
        try:
            if not agents or not isinstance(agents, list) or not user_input:
                return {
                    "error": "Both 'agents' (non-empty list) and 'user_input' are required parameters"
                }

            # Find the initial agent (could be determined by some logic)
            initial_agent = agents[0]

            # Run the orchestration
            return await self.run_agent_orchestration(initial_agent, user_input, max_steps)

        except Exception as e:
            return {"error": f"Failed to run complex agent orchestration: {str(e)}"}


# Singleton instance
openai_agent_skills = OpenAIAgentSkills()


async def create_openai_agent(name: str, instructions: str, model: Optional[str] = None,
                             handoff_description: Optional[str] = None, tools: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """Skill to create a new OpenAI agent."""
    return await openai_agent_skills.create_agent(name, instructions, model, handoff_description, tools)


async def create_openai_handoff_agent(name: str, instructions: str, handoff_targets: List[Dict[str, Any]],
                                    model: Optional[str] = None) -> Dict[str, Any]:
    """Skill to create an agent with handoff capabilities."""
    return await openai_agent_skills.create_handoff_agent(name, instructions, handoff_targets, model)


async def create_openai_guardrail_agent(name: str, instructions: str, output_type: Optional[str] = None,
                                      model: Optional[str] = None) -> Dict[str, Any]:
    """Skill to create an agent with guardrail functionality."""
    return await openai_agent_skills.create_guardrail_agent(name, instructions, output_type, model)


async def run_openai_agent_orchestration(initial_agent: Dict[str, Any],
                                       user_input: str, max_steps: Optional[int] = 10) -> Dict[str, Any]:
    """Skill to run an agent orchestration with potential handoffs."""
    return await openai_agent_skills.run_agent_orchestration(initial_agent, user_input, max_steps)


async def add_guardrail_to_openai_agent(agent_config: Dict[str, Any],
                                       guardrail_func_name: str) -> Dict[str, Any]:
    """Skill to add a guardrail function to an existing agent."""
    return await openai_agent_skills.add_guardrail_to_agent(agent_config, guardrail_func_name)


async def create_homework_guardrail(agent_config: Dict[str, Any]) -> Dict[str, Any]:
    """Skill to create and add a homework-specific guardrail to an agent."""
    return await openai_agent_skills.create_homework_guardrail(agent_config)


async def create_complex_agent_orchestration(agents: List[Dict[str, Any]],
                                           user_input: str,
                                           max_steps: Optional[int] = 10) -> Dict[str, Any]:
    """Skill to run a complex agent orchestration with multiple agents, handoffs, and guardrails."""
    return await openai_agent_skills.create_complex_agent_orchestration(agents, user_input, max_steps)


# Example usage
async def main():
    """Example of using the OpenAI Agent skills."""
    print("Testing OpenAI Agent Skills")
    print("=" * 40)

    # Create a simple agent
    agent_result = await create_openai_agent(
        name="Math Tutor",
        instructions="You provide help with math problems. Explain your reasoning at each step and include examples",
        model="gpt-4"
    )
    print(f"Simple agent creation: {agent_result}")

    # Create a history tutor agent
    history_agent_result = await create_openai_agent(
        name="History Tutor",
        instructions="You provide assistance with historical queries. Explain important events and context clearly.",
        handoff_description="Specialist agent for historical questions"
    )
    print(f"History agent creation: {history_agent_result}")

    # Create a triage agent with handoff capabilities
    triage_result = await create_openai_handoff_agent(
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
    print(f"Triage agent with handoffs: {triage_result}")

    # Create a homework guardrail and add it to the triage agent
    if triage_result.get("success"):
        guarded_agent = await create_homework_guardrail(agent_config=triage_result["agent_config"])
        print(f"Agent with homework guardrail: {guarded_agent}")

        # Run the orchestration with guardrail
        orchestration_result = await run_openai_agent_orchestration(
            initial_agent=guarded_agent["updated_agent_config"],
            user_input="who was the first president of the united states?",
            max_steps=5
        )
        print(f"Orchestration result: {orchestration_result}")

        # Test the guardrail with non-homework content
        blocked_result = await run_openai_agent_orchestration(
            initial_agent=guarded_agent["updated_agent_config"],
            user_input="What is the meaning of life?",
            max_steps=5
        )
        print(f"Guardrail blocked result: {blocked_result}")

    # Create a guardrail agent
    guardrail_result = await create_openai_guardrail_agent(
        name="Guardrail check",
        instructions="Check if the user is asking about homework.",
        output_type="HomeworkOutput"
    )
    print(f"Guardrail agent: {guardrail_result}")

    # Add guardrail to existing agent
    if agent_result.get("success") and guardrail_result.get("success"):
        updated_agent = await add_guardrail_to_openai_agent(
            agent_config=agent_result["agent_config"],
            guardrail_func_name="homework_guardrail"
        )
        print(f"Agent with added guardrail: {updated_agent}")

    # Run a complex orchestration
    all_agents = [
        triage_result.get("agent_config", {}),
        agent_result.get("agent_config", {}),
        history_agent_result.get("agent_config", {})
    ]
    complex_result = await create_complex_agent_orchestration(
        agents=all_agents,
        user_input="solve this math equation: 2x + 5 = 15",
        max_steps=5
    )
    print(f"Complex orchestration result: {complex_result}")


if __name__ == "__main__":
    asyncio.run(main())