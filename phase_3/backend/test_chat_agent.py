#!/usr/bin/env python3
"""
Test script to check if the chat agent is working properly.
"""

import os
import sys
import logging

# Add the src directory to the path so imports work correctly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

print("Testing Chat Agent initialization...")

try:
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    logger.info("Environment variables loaded successfully")

    # Check if OPENAI_API_KEY is available
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        print(f"[OK] OPENAI_API_KEY found: {'Yes' if openai_key else 'No'}")
        print(f"  Key length: {len(openai_key) if openai_key else 0} characters")
        print(f"  Key preview: {openai_key[:10]}..." if openai_key else "  Key: None")
    else:
        print("[ERROR] OPENAI_API_KEY not found in environment variables")

    # Try to import and initialize the ChatAgent
    try:
        from src.agents.chat_agent import ChatAgent
        print("\nTrying to initialize ChatAgent...")

        # Create the agent
        agent = ChatAgent()
        print("[OK] ChatAgent initialized successfully!")
        print(f"  Model being used: {agent.model}")

        # Test a simple message processing
        print("\nTesting message processing...")
        test_result = agent.process_message(
            "Add a task to buy groceries",
            "test_user_123"
        )
        print(f"[OK] Message processed successfully!")
        print(f"  Response: {test_result['response']}")
        print(f"  Tool calls: {test_result['tool_calls']}")

        # Check if tool calls were detected
        if test_result['tool_calls']:
            print("[OK] Tool calls detected correctly!")
        else:
            print("[INFO] No tool calls detected - this might be expected depending on the model's interpretation")

    except ImportError as e:
        print(f"[ERROR] Failed to import ChatAgent: {e}")
        print("This suggests that the openai package or other dependencies might not be installed")

    except ValueError as e:
        print(f"[ERROR] ChatAgent initialization failed: {e}")
        print("This is likely due to a missing or invalid OPENAI_API_KEY")

    except Exception as e:
        print(f"[ERROR] Unexpected error initializing ChatAgent: {e}")
        import traceback
        print(f"  Full traceback: {traceback.format_exc()}")

except Exception as e:
    print(f"[ERROR] Failed to load environment variables: {e}")
    import traceback
    print(f"  Full traceback: {traceback.format_exc()}")

print("\nTest completed.")