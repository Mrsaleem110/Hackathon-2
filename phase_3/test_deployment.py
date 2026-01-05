# Test deployment configuration
import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

try:
    # Test importing the api module
    from backend.api import app, handler
    print("✓ Successfully imported api module")
    print("✓ Mangum handler is available")
    print("✓ FastAPI app is configured")

    # Check if all required dependencies are available
    import fastapi
    import mangum
    import sqlmodel
    import google.generativeai
    print("✓ All required dependencies are available")

    print("\nDeployment configuration is ready!")
    print("You can now deploy your application to Vercel or other platforms.")

except ImportError as e:
    print(f"✗ Import error: {e}")
    print("Please make sure all dependencies are installed before deployment.")

except Exception as e:
    print(f"✗ Error: {e}")