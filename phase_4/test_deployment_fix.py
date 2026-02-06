#!/usr/bin/env python3
"""
Verification script to test the deployment fixes
"""

import requests
import json
from urllib.parse import urljoin

def test_deployment():
    base_url = "https://hackathon-2-p-3.vercel.app"

    print("Testing deployed backend endpoints...")

    # Test basic connectivity
    print("\n1. Testing root endpoint:")
    try:
        response = requests.get(f"{base_url}/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")

    # Test health endpoint
    print("\n2. Testing health endpoint:")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")

    # Test routes endpoint to see what's available
    print("\n3. Testing routes endpoint:")
    try:
        response = requests.get(f"{base_url}/debug/routes")
        print(f"   Status: {response.status_code}")
        routes_data = response.json()
        print(f"   Total routes: {routes_data.get('total_routes', 'Unknown')}")

        # Check if tasks routes exist
        all_routes = routes_data.get('all_routes', [])
        tasks_routes = [route for route in all_routes if '/tasks' in route['path']]
        print(f"   Tasks routes found: {len(tasks_routes)}")
        for route in tasks_routes:
            print(f"     - {route['path']} ({', '.join(route['methods'])})")

    except Exception as e:
        print(f"   Error: {e}")

    # Test tasks endpoint (this should now work if backend is fixed)
    print("\n4. Testing tasks endpoint:")
    try:
        response = requests.get(f"{base_url}/tasks/")
        print(f"   Status: {response.status_code}")
        if response.status_code != 405:  # Method Not Allowed
            print(f"   Response: {response.text}")
        else:
            print("   Result: Method Not Allowed (route exists but expects different HTTP method)")
    except Exception as e:
        print(f"   Error: {e}")

    print("\n5. Testing CORS endpoint:")
    try:
        response = requests.get(f"{base_url}/debug/cors")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == "__main__":
    test_deployment()