import requests
import json

def test_login_endpoint():
    """
    Test the login endpoint to see if it's working
    """
    backend_url = "https://hackathon-2-p-3-backend.vercel.app"

    print("Testing login endpoint...")
    print(f"Target URL: {backend_url}/auth/login")

    # Try to login with test credentials
    test_payload = {
        "username": "admin",
        "password": "admin123"
    }

    try:
        response = requests.post(
            f"{backend_url}/auth/login",
            json=test_payload,
            headers={'Content-Type': 'application/json'}
        )

        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

        if response.status_code == 200:
            print("✅ SUCCESS: Login endpoint is working!")
            data = response.json()
            if "access_token" in data:
                print("✅ Token received successfully")
            else:
                print("ℹ️  Response doesn't contain token (might be using different auth system)")
        elif response.status_code == 422:
            print("ℹ️  Endpoint exists but validation failed (expected)")
        elif response.status_code == 401:
            print("ℹ️  Endpoint exists but credentials invalid (expected for wrong credentials)")
        else:
            print(f"❌ Unexpected status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_login_endpoint()