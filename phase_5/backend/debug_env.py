import os
from dotenv import load_dotenv
import sys

print(f"Current working directory: {os.getcwd()}")
print(f"Python path: {sys.path}")

# Check if .env file exists in current directory
import pathlib
env_path = pathlib.Path('.').resolve() / '.env'
print(f".env file exists in current dir: {env_path.exists()}")

# Load environment variables
print("Calling load_dotenv()...")
result = load_dotenv()
print(f"load_dotenv() returned: {result}")

print("\nEnvironment variables after loading:")
all_env_vars = {k: v for k, v in os.environ.items() if 'API_KEY' in k or 'OPENAI' in k}
for k, v in all_env_vars.items():
    print(f"{k}: {v[:50]}...")

print(f"\nSpecific OPENAI_API_KEY: {os.getenv('OPENAI_API_KEY')[:50] if os.getenv('OPENAI_API_KEY') else 'NOT FOUND'}")

# Test importing and creating the chat agent
try:
    from src.agents.chat_agent import ChatAgent
    print("\nTrying to initialize ChatAgent...")
    agent = ChatAgent()
    print("ChatAgent initialized successfully!")
    print(f"Model being used: {agent.model}")
    print(f"Agent's API key starts with: {agent.client.api_key[:20] if hasattr(agent.client, 'api_key') else 'N/A'}...")
except Exception as e:
    print(f"Error initializing ChatAgent: {e}")
    import traceback
    traceback.print_exc()