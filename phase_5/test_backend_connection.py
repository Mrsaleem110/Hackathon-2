import requests
import sys

def test_backend_connection(base_url):
    """
    Test the backend connection to see if the API is accessible
    """
    print(f"Testing backend connection to: {base_url}")

    # Test the root endpoint
    try:
        response = requests.get(f"{base_url}/")
        print(f"Root endpoint (/) - Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        else:
            print(f"Error response: {response.text}")
    except Exception as e:
        print(f"Error connecting to root endpoint: {e}")

    print("\n" + "="*50 + "\n")

    # Test the health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Health endpoint (/health) - Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        else:
            print(f"Error response: {response.text}")
    except Exception as e:
        print(f"Error connecting to health endpoint: {e}")

    print("\n" + "="*50 + "\n")

    # Test the auth endpoints
    auth_endpoints = ["/auth", "/auth/login", "/auth/register", "/auth/me"]
    for endpoint in auth_endpoints:
        try:
            # Use GET for testing, though login/register require POST
            response = requests.get(f"{base_url}{endpoint}")
            print(f"Auth endpoint ({endpoint}) - Status: {response.status_code}")
            # We expect 405 (Method Not Allowed) for POST-only endpoints when using GET
            if response.status_code == 405:
                print(f"  -> This endpoint exists but requires POST method")
            elif response.status_code == 404:
                print(f"  -> This endpoint does not exist")
            else:
                print(f"  -> Response: {response.text[:200]}..." if len(response.text) > 200 else f"  -> Response: {response.text}")
        except Exception as e:
            print(f"Error connecting to {endpoint}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_backend_connection.py <backend_url>")
        print("Example: python test_backend_connection.py https://hackathon-2-phase-3-backend.vercel.app")
        sys.exit(1)

    backend_url = sys.argv[1]
    test_backend_connection(backend_url)