#!/usr/bin/env python3
"""
Test script to verify backend is returning JSON instead of HTML
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

import json
from fastapi.testclient import TestClient
from backend.src.api.main import app

# Create a test client
client = TestClient(app)

def test_endpoint(method, path, expected_status=None):
    """Test an endpoint and check if response is JSON"""
    print(f"\n{'='*60}")
    print(f"Testing: {method} {path}")
    print('='*60)
    
    try:
        if method.upper() == "GET":
            response = client.get(path)
        elif method.upper() == "POST":
            response = client.post(path, json={})
        else:
            response = client.request(method, path)
        
        status_code = response.status_code
        print(f"Status Code: {status_code}")
        
        # Check content type
        content_type = response.headers.get('content-type', '')
        print(f"Content-Type: {content_type}")
        
        # Try to parse as JSON
        try:
            data = response.json()
            print(f"✓ Response is valid JSON")
            print(f"Response body: {json.dumps(data, indent=2)}")
        except json.JSONDecodeError:
            print(f"✗ Response is NOT valid JSON")
            print(f"Response text (first 500 chars): {response.text[:500]}")
            return False
        
        return True
    
    except Exception as e:
        print(f"✗ Error testing endpoint: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("BACKEND JSON RESPONSE VERIFICATION TEST")
    print("="*60)
    
    tests = [
        ("GET", "/", 200),
        ("GET", "/health", 200),
        ("GET", "/debug/test", 200),
        ("GET", "/tasks/", 401),  # Should return JSON error, not HTML
        ("GET", "/nonexistent", 404),  # Should return JSON 404, not HTML
        ("POST", "/auth/login", 400),  # Missing credentials, should return JSON error
    ]
    
    passed = 0
    failed = 0
    
    for method, path, expected_status in tests:
        if test_endpoint(method, path, expected_status):
            passed += 1
        else:
            failed += 1
    
    print("\n" + "="*60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("="*60)
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
