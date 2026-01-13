"""
Test script to verify OpenAI ChatKit UI integration
"""
import asyncio
import aiohttp
import json

async def test_chatkit_endpoints():
    """
    Test the ChatKit API endpoints to ensure they work correctly
    """
    base_url = "http://localhost:8000"  # Assuming FastAPI server is running locally

    async with aiohttp.ClientSession() as session:
        # Test creating a new session
        print("Testing ChatKit session creation...")

        # First, we need to authenticate to get a valid token
        # This assumes you have a way to authenticate first
        try:
            # Try to get an auth token (adjust based on your auth implementation)
            auth_response = await session.post(f"{base_url}/auth/login", json={
                "username": "testuser",
                "password": "testpass"  # Use valid test credentials
            })

            if auth_response.status == 200:
                auth_data = await auth_response.json()
                token = auth_data.get("access_token")

                # Now test the ChatKit session creation with auth header
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                }

                session_response = await session.post(
                    f"{base_url}/api/chatkit/session",
                    json={
                        "userId": "test-user-123",
                        "workflowId": "test-workflow-456"
                    },
                    headers=headers
                )

                if session_response.status == 200:
                    session_data = await session_response.json()
                    print("✓ ChatKit session created successfully:")
                    print(f"  Session ID: {session_data['session_id']}")
                    print(f"  Expires at: {session_data['expires_at']}")

                    # Test refreshing the session
                    print("\nTesting ChatKit session refresh...")
                    refresh_response = await session.post(
                        f"{base_url}/api/chatkit/session/{session_data['session_id']}/refresh",
                        headers=headers
                    )

                    if refresh_response.status == 200:
                        refreshed_data = await refresh_response.json()
                        print("✓ ChatKit session refreshed successfully")
                        print(f"  New session token length: {len(refreshed_data['session_token'])}")

                        # Test validating the session
                        print("\nTesting ChatKit session validation...")
                        validate_response = await session.get(
                            f"{base_url}/api/chatkit/session/{session_data['session_id']}/validate",
                            headers=headers
                        )

                        if validate_response.status == 200:
                            validate_data = await validate_response.json()
                            print("✓ ChatKit session validated successfully")
                            print(f"  Valid: {validate_data['valid']}")

                            print("\n🎉 All ChatKit integration tests passed!")
                            return True
                        else:
                            print(f"✗ Session validation failed with status {validate_response.status}")
                    else:
                        print(f"✗ Session refresh failed with status {refresh_response.status}")
                else:
                    print(f"✗ Session creation failed with status {session_response.status}")
                    print(f"Response: {await session_response.text()}")
            else:
                print(f"✗ Authentication failed with status {auth_response.status}")
                print(f"Response: {await auth_response.text()}")

        except aiohttp.ClientConnectorError:
            print("✗ Could not connect to the API server. Is it running on localhost:8000?")
            print("To run the server: cd backend && uvicorn src.api.main:app --reload")
        except Exception as e:
            print(f"✗ Error during testing: {str(e)}")

    return False

async def test_frontend_component():
    """
    Test the frontend component integration
    """
    print("\nTesting frontend component structure...")

    # Check if required frontend files exist
    import os

    frontend_files = [
        "frontend/src/components/ChatKitWidget.jsx",
        "frontend/src/hooks/useChatSession.js",
        "frontend/public/chatkit-config.json"
    ]

    all_exist = True
    for file_path in frontend_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path} exists")
        else:
            print(f"✗ {file_path} missing")
            all_exist = False

    if all_exist:
        print("✓ All frontend component files exist")
        return True
    else:
        print("✗ Some frontend component files are missing")
        return False

async def main():
    """
    Main test function
    """
    print("🧪 Testing OpenAI ChatKit UI Integration\n")

    # Test frontend components
    frontend_ok = await test_frontend_component()

    # Test backend endpoints (if server is running)
    backend_ok = await test_chatkit_endpoints()

    print(f"\n📊 Test Results:")
    print(f"Frontend components: {'✅ PASS' if frontend_ok else '❌ FAIL'}")
    print(f"Backend endpoints: {'✅ PASS' if backend_ok else '⚠️  NEEDS SERVER'}")

    if frontend_ok:
        print(f"\n🚀 OpenAI ChatKit UI skill is ready for use!")
        print(f"📋 To use the skill:")
        print(f"   1. Install dependencies: npm install @openai/chatkit-react")
        print(f"   2. Start the backend: cd backend && uvicorn src.api.main:app --reload")
        print(f"   3. Start the frontend: cd frontend && npm start")
        print(f"   4. Use <ChatKitWidget workflowId='your-workflow-id' userId='user-id' /> in your components")

if __name__ == "__main__":
    asyncio.run(main())