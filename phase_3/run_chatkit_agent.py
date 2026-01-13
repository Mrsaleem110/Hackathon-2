#!/usr/bin/env python3
"""
Script to run the OpenAI ChatKit UI Agent independently
"""
import asyncio
import sys
from pathlib import Path

# Add the project root to the path so imports work correctly
project_root = Path(__file__).parent / "mcp"
sys.path.insert(0, str(project_root))

async def run_chatkit_agent():
    """
    Run the OpenAI ChatKit UI Agent independently
    """
    print("Initializing OpenAI ChatKit UI Agent...")

    # Import the agent manager and register the agent directly
    from src.agents.agent_manager import get_agent_manager, AgentConfig, AgentType
    from src.agents.openai_chatkit_ui_agent import get_chatkit_agent

    # Create the agent instance
    agent = get_chatkit_agent()

    # Create agent config
    agent_config = AgentConfig(
        name="openai_chatkit_ui_agent",
        agent_type=AgentType.CUSTOM,
        description="OpenAI ChatKit UI Implementer - Handles ChatKit session management and UI integration",
        capabilities=[
            "create-chatkit-session",
            "refresh-chatkit-session",
            "get-workflow-details",
            "manage-client-secrets",
            "embed-chatkit-ui"
        ],
        max_concurrent_tasks=10,
        timeout_seconds=60
    )

    # Register with the agent manager directly
    agent_manager = get_agent_manager()
    agent_id = agent_manager.register_agent(agent_config)

    print(f"✓ OpenAI ChatKit UI Agent registered successfully!")
    print(f"  - Agent ID: {agent_id}")
    print(f"  - Agent Name: {agent_config.name}")
    print(f"  - Capabilities: {len(agent_config.capabilities)}")

    # The agent is now ready to handle tasks
    print(f"\n✓ OpenAI ChatKit UI Agent is ready to handle requests!")

    # Return the agent for further use if needed
    return agent

if __name__ == "__main__":
    print("Starting OpenAI ChatKit UI Agent...")
    print("=" * 50)

    try:
        agent = asyncio.run(run_chatkit_agent())
        print("\nAgent is running and ready to handle requests!")
        print("Use the execute_chatkit_task() function to send tasks to the agent.")
    except Exception as e:
        print(f"\n✗ Error running OpenAI ChatKit UI Agent: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)