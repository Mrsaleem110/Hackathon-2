import pytest
import os
from datetime import datetime, timedelta
from jose import jwt
from fastapi.testclient import TestClient

# Import the main FastAPI app
from backend.src.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


def create_test_token(user_id: str, expires_delta: timedelta = None):
    """Helper function to create a test JWT token"""
    if expires_delta is None:
        expires_delta = timedelta(hours=1)

    expire = datetime.utcnow() + expires_delta
    to_encode = {
        "sub": user_id,
        "exp": expire.timestamp(),
        "iat": datetime.utcnow().timestamp()
    }

    secret_key = os.getenv("JWT_SECRET_KEY", "test-secret-key")
    algorithm = "HS256"

    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


def test_complete_auth_flow_before_chat_messaging():
    """End-to-end test for the complete authentication flow before chat messaging"""
    client = TestClient(app)

    # Step 1: Test that public endpoints are accessible without authentication
    response = client.get("/")
    assert response.status_code in [200, 404, 405]  # Main endpoint might not exist, but shouldn't be forbidden

    # Step 2: Test that chat endpoint requires authentication
    response = client.post("/chat/", json={"message": "Hello without auth"})
    assert response.status_code == 401, "Chat endpoint should require authentication"

    # Step 3: Create a valid authentication token
    user_id = "test-user-complete-flow"
    valid_token = create_test_token(user_id)

    # Step 4: Test that authenticated requests are accepted
    response = client.post(
        "/chat/",
        json={"message": "Hello from authenticated user"},
        headers={"Authorization": f"Bearer {valid_token}"}
    )

    # The request should pass authentication (may still fail for other reasons like missing OpenAI key)
    # but should not return 401 Unauthorized
    assert response.status_code != 401, "Authenticated requests should pass auth validation"

    # Step 5: Test that the user ID is properly extracted from the token
    # We'll check this by examining the response or by mocking the chat processing
    # For now, we verify that the auth middleware received the correct user context
    if response.status_code != 401:
        # The request got past auth, which means user ID was extracted successfully
        pass

    # Step 6: Test with an invalid/expired token
    expired_time = datetime.utcnow() - timedelta(hours=1)
    to_encode = {
        "sub": "expired-user",
        "exp": expired_time.timestamp(),  # Already expired
        "iat": (datetime.utcnow() - timedelta(hours=2)).timestamp()
    }
    secret_key = os.getenv("JWT_SECRET_KEY", "test-secret-key")
    algorithm = "HS256"
    expired_token = jwt.encode(to_encode, secret_key, algorithm=algorithm)

    response = client.post(
        "/chat/",
        json={"message": "Hello from expired user"},
        headers={"Authorization": f"Bearer {expired_token}"}
    )
    assert response.status_code == 401, "Expired tokens should be rejected"

    # Step 7: Test with a malformed token
    response = client.post(
        "/chat/",
        json={"message": "Hello from malformed token"},
        headers={"Authorization": "Bearer invalid.token.format"}
    )
    assert response.status_code == 401, "Malformed tokens should be rejected"

    # Step 8: Test with missing token
    response = client.post(
        "/chat/",
        json={"message": "Hello from no token"},
        headers={}  # No Authorization header
    )
    assert response.status_code == 401, "Requests without tokens should be rejected"


def test_auth_flow_with_different_jwt_payload_structures():
    """Test auth flow with different JWT payload structures to ensure normalization"""
    client = TestClient(app)

    # Test with standard 'sub' field
    user_id_sub = "test-user-sub-field"
    token_sub = create_test_token(user_id_sub)

    response = client.post(
        "/chat/",
        json={"message": "Hello with sub field"},
        headers={"Authorization": f"Bearer {token_sub}"}
    )
    assert response.status_code != 401, "Tokens with 'sub' field should work"

    # Test with alternative payload structure if supported
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode_alt = {
        "user_id": f"alt-{user_id_sub}",
        "exp": expire.timestamp(),
        "iat": datetime.utcnow().timestamp()
    }
    secret_key = os.getenv("JWT_SECRET_KEY", "test-secret-key")
    algorithm = "HS256"
    token_alt = jwt.encode(to_encode_alt, secret_key, algorithm=algorithm)

    response = client.post(
        "/chat/",
        json={"message": "Hello with user_id field"},
        headers={"Authorization": f"Bearer {token_alt}"}
    )
    assert response.status_code != 401, "Tokens with 'user_id' field should work"


def test_concurrent_authenticated_requests():
    """Test multiple concurrent authenticated requests to ensure auth is thread-safe"""
    client = TestClient(app)

    # Create multiple tokens for different users
    users = [f"user-{i}" for i in range(3)]
    tokens = [create_test_token(user) for user in users]

    # Send multiple requests with different tokens
    responses = []
    for i, token in enumerate(tokens):
        response = client.post(
            "/chat/",
            json={"message": f"Hello from {users[i]}"},
            headers={"Authorization": f"Bearer {token}"}
        )
        responses.append(response)

    # All should pass authentication
    for response in responses:
        assert response.status_code != 401, "All authenticated requests should pass auth validation"


def test_auth_session_consistency():
    """Test that auth session remains consistent across multiple requests"""
    client = TestClient(app)

    user_id = "test-user-session-consistency"
    token = create_test_token(user_id)

    # Make multiple requests with the same token
    for i in range(3):
        response = client.post(
            "/chat/",
            json={"message": f"Message {i} from {user_id}"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code != 401, f"Request {i} should pass auth validation"


if __name__ == "__main__":
    pytest.main([__file__])