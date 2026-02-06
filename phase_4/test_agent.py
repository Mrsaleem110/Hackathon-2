#!/usr/bin/env python3
"""
Test script to verify the ChatAgent functionality
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.src.agents.chat_agent import ChatAgent

def test_agent():
    print("Testing ChatAgent...")

    try:
        # Initialize the agent
        agent = ChatAgent()
        print("[SUCCESS] ChatAgent initialized successfully")

        # Test a simple message
        result = agent.process_message(
            user_message="Please add a task called 'Buy groceries' with description 'Need to buy milk, bread and eggs'",
            user_id="test_user_123"
        )

        print(f"[SUCCESS] Agent processed message successfully")
        print(f"Response: {result['response']}")
        print(f"Tool calls: {result['tool_calls']}")

        # Test with conversation history
        conversation_history = [
            {"role": "user", "content": "I want to add a task"},
            {"role": "assistant", "content": "Sure, what would you like to add?"}
        ]

        result_with_history = agent.process_message(
            user_message="Add a task called 'Walk the dog'",
            user_id="test_user_123",
            conversation_history=conversation_history
        )

        print(f"\n[SUCCESS] Agent processed message with history successfully")
        print(f"Response: {result_with_history['response']}")
        print(f"Tool calls: {result_with_history['tool_calls']}")

        return True

    except Exception as e:
        print(f"[ERROR] Error testing ChatAgent: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_agent()