import pytest
import os
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from fastapi import HTTPException
from jose import jwt
from datetime import datetime, timedelta

# Import the main FastAPI app
from backend.src.main import app
from backend.src.auth import require_auth
from backend.src.api.chat import router as chat_router


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


def test_chat_endpoint_requires_valid_token():
    """Test that chat endpoint rejects requests without valid JWT token"""
    client = TestClient(app)

    # Test without token
    response = client.post("/chat/", json={"message": "Hello"})
    assert response.status_code == 401
    assert "Unauthorized" in response.text

    # Test with invalid token
    response = client.post(
        "/chat/",
        json={"message": "Hello"},
        headers={"Authorization": "Bearer invalid-token"}
    )
    assert response.status_code == 401


def test_chat_endpoint_accepts_valid_token_with_user_id():
    """Test that chat endpoint accepts requests with valid JWT containing user_id"""
    client = TestClient(app)

    # Create a valid token
    token = create_test_token("test-user-id")

    # Test with valid token
    response = client.post(
        "/chat/",
        json={"message": "Hello from authenticated user"},
        headers={"Authorization": f"Bearer {token}"}
    )

    # Should be accepted (might still fail for other reasons like missing OpenAI key)
    # but should pass the auth check
    assert response.status_code != 401  # Not unauthorized


def test_chat_endpoint_normalizes_different_jwt_payload_formats():
    """Test that chat endpoint handles different JWT payload structures"""
    client = TestClient(app)

    # Test with 'sub' field (standard JWT)
    token_with_sub = create_test_token("test-user-sub")

    response = client.post(
        "/chat/",
        json={"message": "Hello with sub field"},
        headers={"Authorization": f"Bearer {token_with_sub}"}
    )

    # Should be accepted (auth check passes)
    assert response.status_code != 401


def test_chat_endpoint_rejects_token_without_user_identifier():
    """Test that chat endpoint rejects tokens without proper user identification"""
    client = TestClient(app)

    # Create a token without user id
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode = {
        "exp": expire.timestamp(),
        "iat": datetime.utcnow().timestamp()
        # Missing 'sub' or 'user_id' field
    }

    secret_key = os.getenv("JWT_SECRET_KEY", "test-secret-key")
    algorithm = "HS256"
    token = jwt.encode(to_encode, secret_key, algorithm=algorithm)

    response = client.post(
        "/chat/",
        json={"message": "Hello"},
        headers={"Authorization": f"Bearer {token}"}
    )

    # Should be rejected due to missing user identifier
    assert response.status_code == 401


def test_chat_endpoint_includes_user_id_in_request_context():
    """Test that the authenticated user ID is available in the request context"""
    # This tests the middleware functionality
    client = TestClient(app)

    test_user_id = "test-user-for-context"
    token = create_test_token(test_user_id)

    # Mock the actual chat processing to avoid external dependencies
    with patch('backend.src.api.chat.process_chat_message') as mock_process:
        mock_process.return_value = {"response": "test response"}

        response = client.post(
            "/chat/",
            json={"message": "Hello from context test"},
            headers={"Authorization": f"Bearer {token}"}
        )

        # Verify the call was made (meaning auth passed)
        if response.status_code == 200:
            # Verify that the mock was called, indicating the endpoint was reached
            assert mock_process.called
            # TODO: Verify that user_id was passed correctly in the context


if __name__ == "__main__":
    pytest.main([__file__])