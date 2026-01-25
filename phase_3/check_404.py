#!/usr/bin/env python3
"""Check 404 errors - simulate what browser is requesting"""
import requests
import json

BASE_URL = "http://localhost:8001"

# Test different GET requests that might be causing 404
endpoints_to_test = [
    "/auth/login",
    "/auth/register", 
    "/auth/me",
    "/auth/test",
    "/",
    "/health",
    "/debug/routes",
    "/debug/cors",
]

print("=" * 60)
print("Testing GET requests to identify 404s")
print("=" * 60)

for endpoint in endpoints_to_test:
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", timeout=2)
        status = response.status_code
        status_text = "✓ OK" if status == 200 else f"✗ {status}"
        print(f"{status_text:10} GET {endpoint}")
    except Exception as e:
        print(f"ERROR      GET {endpoint} - {str(e)}")

print("\n" + "=" * 60)
print("Testing POST requests (should all fail with 405 or work)")
print("=" * 60)

post_endpoints = [
    ("/auth/login", {"email": "test@example.com", "password": "test"}),
    ("/auth/register", {"email": "test@example.com", "password": "test", "name": "Test"}),
]

for endpoint, data in post_endpoints:
    try:
        response = requests.post(f"{BASE_URL}{endpoint}", json=data, timeout=2)
        status = response.status_code
        status_text = "✓ OK" if status == 200 else f"✗ {status}"
        print(f"{status_text:10} POST {endpoint}")
    except Exception as e:
        print(f"ERROR      POST {endpoint} - {str(e)}")
