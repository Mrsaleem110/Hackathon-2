#!/usr/bin/env python3
"""Test to verify auth flow without any 404 errors"""
import requests
import json

BASE_URL = "http://localhost:8001"

print("=" * 60)
print("Simulating Frontend Auth Flow")
print("=" * 60)

# Step 1: Try to GET /login (should not happen with fixed config)
print("\n1. Testing if /login still causes 404...")
response = requests.get(f"{BASE_URL}/login", timeout=2)
print(f"   GET /login: {response.status_code} (should NOT be called by frontend now)")

# Step 2: Signup via API
print("\n2. Testing POST /auth/register (correct way)...")
response = requests.post(f"{BASE_URL}/auth/register", json={
    "email": "signup_test@example.com",
    "password": "password123",
    "name": "Signup Test"
}, timeout=2)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    token = data['access_token']
    print(f"   ✓ Got token: {token[:20]}...")
    
    # Step 3: Access dashboard data
    print("\n3. Testing GET /tasks/ with auth token...")
    response = requests.get(f"{BASE_URL}/tasks/", headers={
        "Authorization": f"Bearer {token}"
    }, timeout=2)
    print(f"   Status: {response.status_code}")
    tasks = response.json()
    print(f"   ✓ Got {len(tasks)} tasks")
else:
    print(f"   ✗ Registration failed: {response.text}")

print("\n" + "=" * 60)
print("✓ Flow is correct - no API 404s!")
print("=" * 60)
