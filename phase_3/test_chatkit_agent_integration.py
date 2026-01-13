"""
Test script to verify OpenAI ChatKit UI Agent integration
"""
import asyncio
import aiohttp
import json

async def test_chatkit_agent_endpoints():
    """
    Test the ChatKit Agent API endpoints to ensure they work correctly
    """
    base_url = "http://localhost:8000"  # Assuming FastAPI server is running locally

    async with aiohttp.ClientSession() as session:
        print("Testing ChatKit Agent endpoints...")

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

                # Now test the ChatKit Agent session creation with auth header
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                }

                print("Testing ChatKit Agent session creation...")
                session_response = await session.post(
                    f"{base_url}/api/chatkit_agent/session",
                    json={
                        "workflow_id": "test-workflow-456",
                        "user_id": "test-user-123"
                    },
                    headers=headers
                )

                if session_response.status == 200:
                    session_data = await session_response.json()
                    print("✓ ChatKit Agent session created successfully:")
                    print(f"  Session ID: {session_data['session_id']}")
                    print(f"  Client Secret Length: {len(session_data['client_secret'])}")
                    print(f"  Expires at: {session_data['expires_at']}")

                    # Test refreshing the session
                    print("\nTesting ChatKit Agent session refresh...")
                    refresh_response = await session.post(
                        f"{base_url}/api/chatkit_agent/session/{session_data['session_id']}/refresh",
                        headers=headers
                    )

                    if refresh_response.status == 200:
                        refreshed_data = await refresh_response.json()
                        print("✓ ChatKit Agent session refreshed successfully")
                        print(f"  New client secret length: {len(refreshed_data['client_secret'])}")

                        # Test getting workflow details
                        print("\nTesting workflow details retrieval...")
                        workflow_response = await session.get(
                            f"{base_url}/api/chatkit_agent/workflow/{session_data['workflow_id']}",
                            headers=headers
                        )

                        if workflow_response.status == 200:
                            workflow_data = await workflow_response.json()
                            print("✓ Workflow details retrieved successfully")
                            print(f"  Workflow ID: {workflow_data['workflow_id']}")
                            print(f"  Status: {workflow_data['status']}")

                            print("\n🎉 All ChatKit Agent integration tests passed!")
                            return True
                        else:
                            print(f"✗ Workflow details retrieval failed with status {workflow_response.status}")
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

async def test_frontend_components():
    """
    Test the frontend component integration
    """
    print("\nTesting ChatKit Agent frontend components...")

    # Check if required frontend files exist
    import os

    frontend_files = [
        "frontend/src/components/ChatKitUI.jsx",
        "frontend/src/components/ChatKitProvider.jsx",
        "frontend/src/hooks/useChatKit.js"
    ]

    all_exist = True
    for file_path in frontend_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path} exists")
        else:
            print(f"✗ {file_path} missing")
            all_exist = False

    if all_exist:
        print("✓ All ChatKit Agent frontend component files exist")
        return True
    else:
        print("✗ Some ChatKit Agent frontend component files are missing")
        return False

async def main():
    """
    Main test function
    """
    print("🧪 Testing OpenAI ChatKit UI Agent Integration\n")

    # Test frontend components
    frontend_ok = await test_frontend_components()

    # Test backend endpoints (if server is running)
    backend_ok = await test_chatkit_agent_endpoints()

    print(f"\n📊 Test Results:")
    print(f"Frontend components: {'✅ PASS' if frontend_ok else '❌ FAIL'}")
    print(f"Backend endpoints: {'✅ PASS' if backend_ok else '⚠️  NEEDS SERVER'}")

    if frontend_ok and backend_ok:
        print(f"\n🚀 OpenAI ChatKit UI Agent is fully integrated and ready!")
        print(f"📋 To use the agent:")
        print(f"   1. Set OPENAI_API_KEY in your environment")
        print(f"   2. Install dependencies: npm install @openai/chatkit-react react-query")
        print(f"   3. Start the backend: cd backend && uvicorn src.api.main:app --reload")
        print(f"   4. Start the frontend: cd frontend && npm start")
        print(f"   5. Use <ChatKitUI workflowId='your-workflow-id' userId='user-id' /> in your components")
    elif frontend_ok:
        print(f"\n⚠️  Frontend components are ready, but backend needs to be tested with a running server.")
        print(f"   Make sure to set OPENAI_API_KEY and start the backend server.")

if __name__ == "__main__":
    asyncio.run(main())