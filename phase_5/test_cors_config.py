#!/usr/bin/env python3
"""
Test script to verify CORS configuration between your frontend and backend
"""
import requests
import sys

def test_cors_configuration(frontend_url, backend_url):
    """Test CORS configuration between frontend and backend"""
    print(f"Testing CORS configuration:")
    print(f"Frontend: {frontend_url}")
    print(f"Backend: {backend_url}")
    print("-" * 50)

    # Test preflight request (OPTIONS) to auth endpoint
    headers = {
        'Origin': frontend_url,
        'Access-Control-Request-Method': 'POST',
        'Access-Control-Request-Headers': 'Content-Type, Authorization'
    }

    auth_endpoint = f"{backend_url}/auth/login"
    print(f"Testing preflight request to: {auth_endpoint}")

    try:
        response = requests.options(auth_endpoint, headers=headers, timeout=10)

        print(f"Status Code: {response.status_code}")
        print(f"Response Headers:")
        for header, value in response.headers.items():
            print(f"  {header}: {value}")

        # Check for CORS headers
        cors_headers = dict(response.headers)
        allowed_origin = cors_headers.get('Access-Control-Allow-Origin', 'Not Found')

        print(f"\nCORS Check:")
        if allowed_origin == frontend_url or allowed_origin == '*':
            print(f"✅ CORS is properly configured for {frontend_url}")
            return True
        elif allowed_origin == 'Not Found':
            print(f"❌ CORS headers are missing")
            return False
        else:
            print(f"❌ CORS mismatch: expecting {frontend_url}, got {allowed_origin}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False

def test_backend_health(backend_url):
    """Test if backend is healthy"""
    print(f"\nTesting backend health: {backend_url}/health")

    try:
        response = requests.get(f"{backend_url}/health", timeout=10)
        print(f"Health check status: {response.status_code}")

        if response.status_code == 200:
            try:
                health_data = response.json()
                print(f"Health data: {health_data}")
                return True
            except:
                print(f"Health response (non-JSON): {response.text[:200]}...")
                return True
        else:
            print(f"❌ Backend health check failed: {response.text[:200]}...")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend health check failed: {e}")
        return False

def main():
    # Your specific URLs
    FRONTEND_URL = "https://hackathon-2-p-3-frontend.vercel.app"
    BACKEND_URL = "https://hackathon-2-p-3-backend.vercel.app"

    print("CORS Configuration Diagnostic Tool")
    print("=" * 50)

    # Test backend health first
    backend_ok = test_backend_health(BACKEND_URL)

    if backend_ok:
        # Test CORS configuration
        cors_ok = test_cors_configuration(FRONTEND_URL, BACKEND_URL)

        print("\n" + "=" * 50)
        if cors_ok:
            print("✅ CORS configuration is working correctly!")
            print("Your authentication requests should now work.")
        else:
            print("❌ CORS configuration needs to be fixed!")
            print("Update your backend environment variables as follows:")
            print(f"CORS_ORIGINS={FRONTEND_URL},https://*.vercel.app")
            print(f"FRONTEND_URL={FRONTEND_URL}")
            print(f"BETTER_AUTH_URL={FRONTEND_URL}")
    else:
        print(f"❌ Backend is not accessible. Please check if {BACKEND_URL} is running.")

if __name__ == "__main__":
    main()