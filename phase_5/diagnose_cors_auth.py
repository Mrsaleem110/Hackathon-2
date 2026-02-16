#!/usr/bin/env python3
"""
Diagnosis script for CORS and authentication issues
"""
import requests
import sys
import os
from urllib.parse import urljoin

def check_backend_health(backend_url):
    """Check if backend is reachable and healthy"""
    try:
        health_url = urljoin(backend_url, "/health")
        response = requests.get(health_url, timeout=10)
        if response.status_code == 200:
            print(f"✓ Backend health check passed: {response.json()}")
            return True
        else:
            print(f"✗ Backend health check failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"✗ Backend is unreachable: {str(e)}")
        return False

def check_cors_preflight(backend_url, frontend_url):
    """Test CORS preflight request"""
    try:
        headers = {
            'Origin': frontend_url,
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'Content-Type, Authorization'
        }

        auth_login_url = urljoin(backend_url, "/auth/login")
        response = requests.options(auth_login_url, headers=headers, timeout=10)

        print(f"CORS Preflight Response Status: {response.status_code}")

        # Check CORS headers
        cors_headers = dict(response.headers)
        allowed_origin = cors_headers.get('Access-Control-Allow-Origin', 'Not Found')
        allow_credentials = cors_headers.get('Access-Control-Allow-Credentials', 'Not Found')

        print(f"Access-Control-Allow-Origin: {allowed_origin}")
        print(f"Access-Control-Allow-Credentials: {allow_credentials}")

        if allowed_origin == frontend_url or allowed_origin == '*':
            print("✓ CORS is properly configured for your frontend")
            return True
        else:
            print(f"✗ CORS mismatch: expecting {frontend_url}, got {allowed_origin}")
            return False

    except Exception as e:
        print(f"✗ CORS check failed: {str(e)}")
        return False

def check_auth_endpoints(backend_url):
    """Check if auth endpoints are accessible"""
    endpoints = [
        ("/auth/test", "GET"),
        ("/auth/login", "POST"),
        ("/auth/register", "POST")
    ]

    for endpoint, method in endpoints:
        try:
            url = urljoin(backend_url, endpoint)
            if method == "GET":
                response = requests.get(url, timeout=10)
            elif method == "POST":
                # Send empty request to check if endpoint exists
                response = requests.post(url, json={}, timeout=10)

            if response.status_code in [200, 400, 401, 422]:  # Expected status codes
                print(f"✓ Auth endpoint {endpoint} is accessible (Status: {response.status_code})")
            else:
                print(f"? Auth endpoint {endpoint} returned unexpected status: {response.status_code}")
        except Exception as e:
            print(f"✗ Auth endpoint {endpoint} is unreachable: {str(e)}")

def main():
    print("CORS and Authentication Diagnostic Tool")
    print("=" * 50)

    # Your specific URLs
    BACKEND_URL = "https://hackathon-2-p-3-backend.vercel.app"
    FRONTEND_URL = "https://hackathon-2-p-3-frontend.vercel.app"

    print(f"Testing CORS between: {FRONTEND_URL} → {BACKEND_URL}")
    print("-" * 50)

    # Test backend health first
    backend_ok = check_backend_health(BACKEND_URL)

    if not backend_ok:
        print("\n❌ Backend is not accessible. Please check:")
        print("   - Is the backend deployed and running?")
        print("   - Are there any deployment errors in Vercel?")
        print("   - Have you set the environment variables correctly?")
        return False

    # Test CORS configuration
    print("\nTesting CORS configuration...")
    cors_ok = check_cors_preflight(BACKEND_URL, FRONTEND_URL)

    # Test auth endpoints
    print("\nTesting auth endpoints...")
    check_auth_endpoints(BACKEND_URL)

    print("\n" + "=" * 50)
    if cors_ok:
        print("✅ CORS configuration appears to be working!")
        print("Your authentication requests should now work.")
    else:
        print("❌ CORS configuration needs to be fixed!")
        print("Check your backend environment variables:")
        print(f"CORS_ORIGINS={FRONTEND_URL},https://*.vercel.app")
        print(f"FRONTEND_URL={FRONTEND_URL}")

if __name__ == "__main__":
    main()