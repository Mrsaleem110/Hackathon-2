#!/usr/bin/env python3
"""
Diagnostic script to check backend deployment status and identify issues
"""
import requests
import sys
import json

def check_backend_status():
    """Check the status of the deployed backend"""
    backend_url = "https://hackathon-2-p-3-backend.vercel.app"

    print("Backend Diagnostic Tool")
    print("=" * 50)
    print(f"Checking: {backend_url}")
    print()

    # Check main endpoint
    print("1. Checking main endpoint...")
    try:
        response = requests.get(f"{backend_url}/", timeout=10)
        print(f"   Status: {response.status_code}")
        try:
            data = response.json()
            print(f"   Response: {json.dumps(data, indent=2)}")
        except:
            print(f"   Raw response: {response.text[:200]}...")
    except Exception as e:
        print(f"   Error: {e}")
    print()

    # Check health endpoint
    print("2. Checking health endpoint...")
    try:
        response = requests.get(f"{backend_url}/health", timeout=10)
        print(f"   Status: {response.status_code}")
        try:
            data = response.json()
            print(f"   Response: {json.dumps(data, indent=2)}")
        except:
            print(f"   Raw response: {response.text[:200]}...")
    except Exception as e:
        print(f"   Error: {e}")
    print()

    # Check debug/test endpoint
    print("3. Checking debug/test endpoint...")
    try:
        response = requests.get(f"{backend_url}/debug/test", timeout=10)
        print(f"   Status: {response.status_code}")
        try:
            data = response.json()
            print(f"   Response: {json.dumps(data, indent=2)}")
        except:
            print(f"   Raw response: {response.text[:200]}...")
    except Exception as e:
        print(f"   Error: {e}")
    print()

    # Check if auth endpoints exist
    print("4. Checking if auth endpoints exist...")
    auth_endpoints = [
        "/auth/test",
        "/auth/login",
        "/auth/register",
        "/auth/me"
    ]

    for endpoint in auth_endpoints:
        try:
            response = requests.get(f"{backend_url}{endpoint}", timeout=10)
            print(f"   {endpoint}: {response.status_code}")
        except Exception as e:
            print(f"   {endpoint}: Error - {e}")
    print()

    # Check debug routes endpoint
    print("5. Checking debug routes endpoint...")
    try:
        response = requests.get(f"{backend_url}/debug/routes", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"   Total routes: {data.get('total_routes', 'unknown')}")
                print(f"   Auth routes: {len(data.get('auth_routes', []))}")
            except:
                print(f"   Could not parse route data")
        else:
            print(f"   Routes endpoint not available")
    except Exception as e:
        print(f"   Error checking routes: {e}")
    print()

    print("=" * 50)
    print("Diagnostic complete.")
    print()
    print("Interpretation:")
    print("- If main endpoint shows 'Super Minimal API - Serverless Ready', the app is in fallback mode")
    print("- If health endpoint shows 'degraded' or 'error', there were import issues")
    print("- If auth endpoints return 404, the auth router failed to load")
    print("- If debug/routes returns route information, the app loaded successfully")

if __name__ == "__main__":
    check_backend_status()