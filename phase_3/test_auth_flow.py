#!/usr/bin/env python3
"""
Test the complete authentication and dashboard flow
"""
import requests
import json
import time

BASE_URL = "http://localhost:8001"

def test_auth_flow():
    """Test registration, login, and API access"""
    
    print("=" * 60)
    print("Testing Authentication Flow")
    print("=" * 60)
    
    # Test 1: Registration
    print("\n1. Testing Registration...")
    register_data = {
        "email": "testuser123@example.com",
        "password": "password123",
        "name": "Test User"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code != 200:
        print("   ✗ Registration failed!")
        return False
    
    registration_data = response.json()
    token = registration_data.get('access_token')
    user = registration_data.get('user')
    
    print(f"   ✓ Registration successful!")
    print(f"   Token: {token[:20]}...")
    print(f"   User: {user}")
    
    # Test 2: Get Current User
    print("\n2. Testing Get Current User...")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code != 200:
        print("   ✗ Get current user failed!")
        return False
    
    print("   ✓ Get current user successful!")
    
    # Test 3: Create a Task
    print("\n3. Testing Create Task...")
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "priority": "high",
        "completed": False
    }
    
    response = requests.post(f"{BASE_URL}/tasks/", json=task_data, headers=headers)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code not in [200, 201]:
        print("   ✗ Create task failed!")
        return False
    
    print("   ✓ Create task successful!")
    
    # Test 4: Get Tasks
    print("\n4. Testing Get Tasks...")
    response = requests.get(f"{BASE_URL}/tasks/", headers=headers)
    print(f"   Status: {response.status_code}")
    tasks = response.json()
    print(f"   Tasks count: {len(tasks)}")
    print(f"   Response: {json.dumps(tasks, indent=2)}")
    
    if response.status_code != 200:
        print("   ✗ Get tasks failed!")
        return False
    
    print("   ✓ Get tasks successful!")
    
    # Test 5: Test Login with same user
    print("\n5. Testing Login...")
    login_data = {
        "email": "testuser123@example.com",
        "password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code != 200:
        print("   ✗ Login failed!")
        return False
    
    login_data_response = response.json()
    new_token = login_data_response.get('access_token')
    
    print("   ✓ Login successful!")
    print(f"   New Token: {new_token[:20]}...")
    
    # Test 6: Get tasks with new token
    print("\n6. Testing Get Tasks with New Token...")
    headers['Authorization'] = f"Bearer {new_token}"
    response = requests.get(f"{BASE_URL}/tasks/", headers=headers)
    print(f"   Status: {response.status_code}")
    tasks = response.json()
    print(f"   Tasks count: {len(tasks)}")
    
    if response.status_code != 200:
        print("   ✗ Get tasks with new token failed!")
        return False
    
    print("   ✓ Get tasks with new token successful!")
    
    print("\n" + "=" * 60)
    print("✓ All tests passed!")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    time.sleep(1)  # Wait for server to be ready
    test_auth_flow()
