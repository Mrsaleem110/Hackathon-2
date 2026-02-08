"""
Final script to check and test the API key properly
"""
import os
from dotenv import load_dotenv

def check_and_test_api_key():
    print("=== Comprehensive API Key Check ===")

    # Load environment variables from .env files
    load_dotenv(override=True)  # Override any existing environment variables

    print("After loading .env files:")
    for key, value in os.environ.items():
        if 'API_KEY' in key.upper() or 'OPENAI' in key.upper():
            print(f"  {key}: {value[:30]}...")

    # Get the API key
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print(f"\nFinal OPENAI_API_KEY from environment: {api_key[:30]}...")
        print(f"Full length: {len(api_key)}")
        print(f"Last 10 chars: ...{api_key[-10:]}")

        # Test the API key
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)

            # Make a minimal test call
            print("Testing API key...")
            models = client.models.list()
            print("SUCCESS: API key is working correctly!")
            return True

        except Exception as e:
            print(f"FAILURE: API key is not working: {e}")
            return False
    else:
        print("No OPENAI_API_KEY found in environment")
        return False

if __name__ == "__main__":
    success = check_and_test_api_key()

    if success:
        print("\n✅ Your API key is correctly configured and working!")
        print("Make sure to restart your backend server to pick up the new API key.")
    else:
        print("\n❌ Your API key is still not working.")
        print("The issue might be:")
        print("1. The API key is invalid/expired")
        print("2. You need to restart your backend server")
        print("3. There might be a system-level environment variable overriding the .env file")