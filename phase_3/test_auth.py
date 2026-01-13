"""
Test script to validate the authentication system
"""
import requests
import json
import os
from datetime import datetime

# Configuration
BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "testpassword123"
TEST_NAME = "Test User"

def test_auth_flow():
    print("🧪 Testing Authentication Flow...")
    print("=" * 50)

    # Step 1: Test registration
    print("\n1. Testing Registration...")
    try:
        register_response = requests.post(
            f"{BASE_URL}/auth/register",
            json={
                "email": TEST_EMAIL,
                "name": TEST_NAME,
                "password": TEST_PASSWORD
            }
        )

        if register_response.status_code == 200:
            print("✅ Registration successful")
            register_data = register_response.json()
            token = register_data["access_token"]
            print(f"   Token received: {token[:20]}...")
        else:
            print(f"❌ Registration failed: {register_response.status_code} - {register_response.text}")
            return False
    except Exception as e:
        print(f"❌ Registration error: {str(e)}")
        return False

    # Step 2: Test protected endpoint with valid token
    print("\n2. Testing Protected Endpoint with Valid Token...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        profile_response = requests.get(f"{BASE_URL}/auth/me", headers=headers)

        if profile_response.status_code == 200:
            print("✅ Profile access successful")
            profile_data = profile_response.json()
            print(f"   User ID: {profile_data['id']}")
            print(f"   Email: {profile_data['email']}")
        else:
            print(f"❌ Profile access failed: {profile_response.status_code} - {profile_response.text}")
            return False
    except Exception as e:
        print(f"❌ Profile access error: {str(e)}")
        return False

    # Step 3: Test login with registered user
    print("\n3. Testing Login with Registered User...")
    try:
        login_response = requests.post(
            f"{BASE_URL}/auth/login",
            json={
                "email": TEST_EMAIL,
                "password": TEST_PASSWORD
            }
        )

        if login_response.status_code == 200:
            print("✅ Login successful")
            login_data = login_response.json()
            new_token = login_data["access_token"]
            print(f"   New token received: {new_token[:20]}...")
        else:
            print(f"❌ Login failed: {login_response.status_code} - {login_response.text}")
            return False
    except Exception as e:
        print(f"❌ Login error: {str(e)}")
        return False

    # Step 4: Test protected endpoint with login token
    print("\n4. Testing Protected Endpoint with Login Token...")
    try:
        headers = {"Authorization": f"Bearer {new_token}"}
        profile_response = requests.get(f"{BASE_URL}/auth/me", headers=headers)

        if profile_response.status_code == 200:
            print("✅ Profile access with login token successful")
        else:
            print(f"❌ Profile access failed: {profile_response.status_code} - {profile_response.text}")
            return False
    except Exception as e:
        print(f"❌ Profile access error: {str(e)}")
        return False

    # Step 5: Test invalid token
    print("\n5. Testing Invalid Token Protection...")
    try:
        headers = {"Authorization": "Bearer invalid_token_here"}
        invalid_response = requests.get(f"{BASE_URL}/auth/me", headers=headers)

        if invalid_response.status_code == 401:
            print("✅ Invalid token protection working correctly")
        else:
            print(f"❌ Invalid token not rejected: {invalid_response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Invalid token test error: {str(e)}")
        return False

    # Step 6: Test refresh token
    print("\n6. Testing Token Refresh...")
    try:
        headers = {"Authorization": f"Bearer {new_token}"}
        refresh_response = requests.post(f"{BASE_URL}/auth/refresh", headers=headers)

        if refresh_response.status_code == 200:
            print("✅ Token refresh successful")
            refresh_data = refresh_response.json()
            refreshed_token = refresh_data["access_token"]
            print(f"   Refreshed token: {refreshed_token[:20]}...")
        else:
            print(f"❌ Token refresh failed: {refresh_response.status_code} - {refresh_response.text}")
            return False
    except Exception as e:
        print(f"❌ Token refresh error: {str(e)}")
        return False

    # Step 7: Test protected chat endpoint
    print("\n7. Testing Protected Chat Endpoint...")
    try:
        headers = {"Authorization": f"Bearer {refreshed_token}", "Content-Type": "application/json"}
        chat_response = requests.post(
            f"{BASE_URL}/api/{profile_data['id']}/chat",
            headers=headers,
            json={
                "message": "Hello, test message!",
                "conversation_id": None
            }
        )

        if chat_response.status_code == 200:
            print("✅ Protected chat endpoint accessible")
            chat_data = chat_response.json()
            print(f"   Conversation ID: {chat_data.get('conversation_id', 'N/A')}")
        else:
            print(f"❌ Protected chat endpoint failed: {chat_response.status_code} - {chat_response.text}")
            return False
    except Exception as e:
        print(f"❌ Chat endpoint test error: {str(e)}")
        return False

    print("\n🎉 All authentication tests passed!")
    return True

def cleanup_test_user():
    """Note: In a real implementation, you might want to clean up test users"""
    print("\n🧹 Test cleanup completed (no cleanup implemented for this test)")
    print("   Note: Test user remains in the database for further testing")

if __name__ == "__main__":
    print(f"🚀 Starting authentication system test at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   Target URL: {BASE_URL}")
    print(f"   Test email: {TEST_EMAIL}")

    success = test_auth_flow()

    if success:
        print(f"\n✅ Authentication system validation completed successfully!")
        cleanup_test_user()
    else:
        print(f"\n❌ Authentication system validation failed!")
        exit(1)