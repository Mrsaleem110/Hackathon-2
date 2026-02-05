#!/usr/bin/env python3
"""
Debug script to check authentication endpoints and diagnose common issues
"""
import requests
import sys
import os
import json
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

def check_auth_endpoints(backend_url):
    """Check if authentication endpoints are available"""
    endpoints = [
        ("/auth/test", "GET"),
        ("/auth/login", "POST"),
        ("/auth/register", "POST"),
        ("/auth/me", "GET")
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
                print(f"✓ Auth endpoint {endpoint} is accessible")
            else:
                print(f"? Auth endpoint {endpoint} returned unexpected status: {response.status_code}")
        except Exception as e:
            print(f"✗ Auth endpoint {endpoint} is unreachable: {str(e)}")

def check_cors_configuration(backend_url, frontend_origin):
    """Check CORS configuration by simulating a cross-origin request"""
    try:
        # Test preflight request
        headers = {
            'Origin': frontend_origin,
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'Content-Type,Authorization'
        }

        cors_test_url = urljoin(backend_url, "/auth/login")
        response = requests.options(cors_test_url, headers=headers, timeout=10)

        cors_headers = response.headers
        if 'Access-Control-Allow-Origin' in cors_headers:
            allowed_origin = cors_headers['Access-Control-Allow-Origin']
            if allowed_origin == frontend_origin or allowed_origin == '*':
                print(f"✓ CORS is properly configured for {frontend_origin}")
            else:
                print(f"✗ CORS mismatch: expecting {frontend_origin}, got {allowed_origin}")
        else:
            print(f"✗ CORS headers missing in response")

    except Exception as e:
        print(f"✗ CORS check failed: {str(e)}")

def test_basic_auth_request(backend_url):
    """Test a basic authentication request"""
    try:
        # Test with invalid credentials to see error format
        login_url = urljoin(backend_url, "/auth/login")
        response = requests.post(login_url, json={
            "email": "test@example.com",
            "password": "invalid_password"
        }, timeout=10)

        print(f"Login endpoint response status: {response.status_code}")
        if response.status_code == 422:  # Validation error
            print("✓ Login endpoint accepts requests (validation error is expected)")
        elif response.status_code in [401, 403]:  # Auth error
            print("✓ Login endpoint accepts requests (auth error is expected)")
        else:
            print(f"? Unexpected response from login endpoint: {response.status_code}")

    except Exception as e:
        print(f"✗ Auth request test failed: {str(e)}")

def main():
    print("Authentication Endpoint Diagnostic Tool")
    print("=" * 50)

    # Get backend URL from environment or command line
    backend_url = os.getenv("BACKEND_URL", input("Enter your backend URL (e.g., https://your-backend.vercel.app): "))
    if not backend_url.startswith(('http://', 'https://')):
        backend_url = 'https://' + backend_url

    frontend_origin = os.getenv("FRONTEND_ORIGIN", input("Enter your frontend origin (e.g., https://your-frontend.vercel.app): "))
    if not frontend_origin.startswith(('http://', 'https://')):
        frontend_origin = 'https://' + frontend_origin

    print(f"\nTesting backend: {backend_url}")
    print(f"Frontend origin: {frontend_origin}")
    print("-" * 30)

    # Run diagnostics
    if check_backend_health(backend_url):
        print("\nChecking authentication endpoints...")
        check_auth_endpoints(backend_url)

        print("\nChecking CORS configuration...")
        check_cors_configuration(backend_url, frontend_origin)

        print("\nTesting basic auth request...")
        test_basic_auth_request(backend_url)
    else:
        print("\n❌ Cannot reach backend. Please check:")
        print("   - Is the backend deployed and running?")
        print("   - Is the URL correct?")
        print("   - Are there any network/firewall issues?")

    print("\nDiagnostic complete.")

if __name__ == "__main__":
    main()