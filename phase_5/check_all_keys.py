"""
Script to check all possible locations where the API key might be stored
"""
import os
import subprocess
import sys

def check_environment_variables():
    print("=== Checking Environment Variables ===")
    for key, value in os.environ.items():
        if 'API_KEY' in key.upper() or 'OPENAI' in key.upper():
            print(f"{key}: {value[:50]}...")
    print()

def check_dotenv_files():
    print("=== Checking .env Files ===")
    env_files = [
        './.env',
        './backend/.env',
        './frontend/.env',
        './backend/src/.env',
        './backend/src/agents/.env'
    ]

    for env_file in env_files:
        try:
            with open(env_file, 'r') as f:
                print(f"\nContents of {env_file}:")
                for i, line in enumerate(f.readlines(), 1):
                    if 'API_KEY' in line or 'OPENAI' in line:
                        print(f"  Line {i}: {line.strip()}")
        except FileNotFoundError:
            print(f"{env_file}: File not found")
    print()

def check_python_code():
    print("=== Checking Python Files for API Keys ===")
    import glob

    # Search for Python files that might contain API keys
    py_files = glob.glob("./backend/**/*.py", recursive=True)

    for py_file in py_files:
        try:
            with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                for i, line in enumerate(lines, 1):
                    if ('OPENAI_API_KEY' in line or 'sk-proj-' in line) and '=' in line:
                        print(f"{py_file}:{i}: {line.strip()}")
        except Exception as e:
            continue  # Skip files that can't be read
    print()

def check_direct_api_key_usage():
    print("=== Testing Current API Key in Environment ===")
    from dotenv import load_dotenv
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print(f"Current OPENAI_API_KEY from environment: {api_key[:30]}...")
        print(f"Full length: {len(api_key)}")
        print(f"Last 10 chars: ...{api_key[-10:]}")

        # Try to use it
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)

            # Make a minimal test call
            models = client.models.list()
            print("✅ API key is working correctly!")

        except Exception as e:
            print(f"❌ API key is not working: {e}")
    else:
        print("No OPENAI_API_KEY found in environment")
    print()

if __name__ == "__main__":
    print("Starting comprehensive API key check...\n")

    check_environment_variables()
    check_dotenv_files()
    check_python_code()
    check_direct_api_key_usage()

    print("=== Check Complete ===")