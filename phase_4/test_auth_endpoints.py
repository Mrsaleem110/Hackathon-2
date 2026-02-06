import requests
import json
import time

def test_auth_endpoints():
    """
    Test script to verify if auth endpoints are working on your deployed backend
    """

    # Replace with your actual deployed backend URL
    BACKEND_URL = "https://hackathon-2-p-3-backend.vercel.app"

    print("🔍 Testing Auth Endpoints on Deployed Backend")
    print("=" * 50)
    print(f"Testing backend: {BACKEND_URL}")
    print()

    # Test 1: Health check
    print("1. Testing /health endpoint...")
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
            print("   ✅ Health endpoint working")
        else:
            print(f"   ❌ Health endpoint failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    print()

    # Test 2: Auth health check
    print("2. Testing /auth/health endpoint...")
    try:
        response = requests.get(f"{BACKEND_URL}/auth/health", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code in [200, 404]:  # 404 is expected if the route doesn't exist
            if response.status_code == 200:
                print(f"   Response: {response.json()}")
                print("   ✅ Auth health endpoint accessible")
            else:
                print("   ℹ️  Auth health endpoint not found (may be normal)")
        else:
            print(f"   ❌ Auth health endpoint failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    print()

    # Test 3: Auth login endpoint (should return 422 for missing body or 405 for GET)
    print("3. Testing /auth/login endpoint...")
    try:
        response = requests.get(f"{BACKEND_URL}/auth/login", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code in [405, 422, 200]:  # Different responses depending on implementation
            print(f"   Response: {response.json() if response.content else 'No content'}")
            if response.status_code in [405, 422]:
                print("   ✅ Auth login endpoint accessible (expected status)")
            else:
                print("   ℹ️  Auth login endpoint returned different status")
        else:
            print(f"   ❌ Auth login endpoint failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    print()

    # Test 4: Debug routes endpoint
    print("4. Testing /debug/routes endpoint...")
    try:
        response = requests.get(f"{BACKEND_URL}/debug/routes", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Total routes: {data.get('total_routes', 'unknown')}")
            print("   ✅ Debug routes endpoint working")
            # Show some route examples
            routes = data.get('routes', [])
            if routes:
                print("   Sample routes:")
                for route in routes[:5]:  # Show first 5 routes
                    print(f"     - {route.get('path', 'unknown')}: {route.get('methods', [])}")
        elif response.status_code == 404:
            print("   ℹ️  Debug routes endpoint not found")
        else:
            print(f"   ❌ Debug routes endpoint failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    print()

    # Test 5: Root endpoint
    print("5. Testing root endpoint...")
    try:
        response = requests.get(f"{BACKEND_URL}/", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
            print("   ✅ Root endpoint working")
        else:
            print(f"   ❌ Root endpoint failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    print()

    print("=" * 50)
    print("Testing complete!")
    print()
    print("Summary:")
    print("- If health and root endpoints work, your backend is running")
    print("- If auth endpoints return 405/422, they exist but expect different request types")
    print("- If auth endpoints return 200 with error messages, they're stub implementations")
    print("- Check Vercel logs for detailed error information if endpoints fail")

if __name__ == "__main__":
    test_auth_endpoints()