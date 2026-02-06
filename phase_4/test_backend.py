import requests
import json

def test_backend_status():
    """Test if the backend is responding properly"""
    backend_url = "https://hackathon-2-p-3-backend.vercel.app"

    print("Testing backend endpoints...")

    # Test health endpoint
    try:
        response = requests.get(f"{backend_url}/health")
        print(f"Health endpoint: {response.status_code}")
        if response.status_code == 200:
            print(f"  Health response: {response.json()}")
        else:
            print(f"  Health error: {response.text}")
    except Exception as e:
        print(f"Health test failed: {e}")

    print()

    # Test root endpoint
    try:
        response = requests.get(f"{backend_url}/")
        print(f"Root endpoint: {response.status_code}")
        if response.status_code == 200:
            print(f"  Root response: {response.json()}")
        else:
            print(f"  Root error: {response.text}")
    except Exception as e:
        print(f"Root test failed: {e}")

    print()

    # Test auth login with sample data
    try:
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        response = requests.post(
            f"{backend_url}/auth/login",
            json=login_data,
            headers={'Content-Type': 'application/json'}
        )
        print(f"Login endpoint: {response.status_code}")
        if response.status_code in [200, 401, 422]:
            print(f"  Login response: {response.text}")
        else:
            print(f"  Login error: {response.text}")
    except Exception as e:
        print(f"Login test failed: {e}")

if __name__ == "__main__":
    test_backend_status()