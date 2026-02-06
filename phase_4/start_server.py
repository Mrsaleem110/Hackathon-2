import os
import sys

# Add the backend directory to the path
sys.path.insert(0, './backend')

# Set required environment variables
os.environ['SECRET_KEY'] = 'very-long-secret-key-for-jwt-tokens-32chars-at-least'
os.environ['DATABASE_URL'] = 'sqlite:///./todo_app_local.db'

print("Environment variables set")

try:
    from backend.src.api.main import app
    print("App imported successfully")

    import uvicorn
    print("Starting server on http://0.0.0.0:8001")

    # Run the server
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")

except Exception as e:
    print(f"Error starting server: {e}")
    import traceback
    traceback.print_exc()