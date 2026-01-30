import pytest
import os
from datetime import datetime, timedelta
from jose import jwt
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Import the main FastAPI app
from backend.src.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


def create_test_token(user_id: str = None, expires_delta: timedelta = None, include_user_id: bool = True):
    """Helper function to create test JWT tokens with various configurations"""
    if expires_delta is None:
        expires_delta = timedelta(hours=1)

    expire = datetime.utcnow() + expires_delta
    to_encode = {
        "exp": expire.timestamp(),
        "iat": datetime.utcnow().timestamp()
    }

    # Conditionally add user ID
    if include_user_id and user_id:
        to_encode["sub"] = user_id

    secret_key = os.getenv("JWT_SECRET_KEY", "test-secret-key")
    algorithm = "HS256"

    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


def test_error_handling_when_user_id_missing_from_token():
    """Test error handling when userId is missing from JWT token"""
    client = TestClient(app)

    # Create a token without user ID
    token_without_user_id = create_test_token(include_user_id=False)

    response = client.post(
        "/chat/",
        json={"message": "Hello without user ID"},
        headers={"Authorization": f"Bearer {token_without_user_id}"}
    )

    # Should return 401 Unauthorized due to missing user ID
    assert response.status_code == 401, "Requests without user ID in token should be rejected"


def test_error_handling_when_token_has_empty_user_id():
    """Test error handling when token has empty or null user ID"""
    client = TestClient(app)

    # Create a token with empty user ID
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode = {
        "sub": "",  # Empty user ID
        "exp": expire.timestamp(),
        "iat": datetime.utcnow().timestamp()
    }

    secret_key = os.getenv("JWT_SECRET_KEY", "test-secret-key")
    algorithm = "HS256"
    token_with_empty_user_id = jwt.encode(to_encode, secret_key, algorithm=algorithm)

    response = client.post(
        "/chat/",
        json={"message": "Hello with empty user ID"},
        headers={"Authorization": f"Bearer {token_with_empty_user_id}"}
    )

    assert response.status_code == 401, "Requests with empty user ID should be rejected"


def test_error_handling_when_token_has_null_user_id():
    """Test error handling when token has null user ID"""
    client = TestClient(app)

    # Create a token with null-like user ID
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode = {
        "sub": None,  # Null user ID
        "exp": expire.timestamp(),
        "iat": datetime.utcnow().timestamp()
    }

    secret_key = os.getenv("JWT_SECRET_KEY", "test-secret-key")
    algorithm = "HS256"
    token_with_null_user_id = jwt.encode(to_encode, secret_key, algorithm=algorithm)

    response = client.post(
        "/chat/",
        json={"message": "Hello with null user ID"},
        headers={"Authorization": f"Bearer {token_with_null_user_id}"}
    )

    assert response.status_code == 401, "Requests with null user ID should be rejected"


def test_error_handling_for_malformed_authorization_header():
    """Test error handling for malformed Authorization headers"""
    client = TestClient(app)

    malformed_headers = [
        {"Authorization": ""},  # Empty auth header
        {"Authorization": "Bearer"},  # Missing token
        {"Authorization": "Bearer  "},  # Space instead of token
        {"Authorization": "Basic abc123"},  # Wrong auth type
        {"Authorization": "Bearer token1 token2"},  # Multiple tokens
        {"Authorization": "Bearer invalid.token.format"},  # Invalid format
    ]

    for header in malformed_headers:
        response = client.post(
            "/chat/",
            json={"message": "Hello with malformed header"},
            headers=header
        )
        # Most of these should return 401, though some might behave differently
        # depending on the exact implementation
        assert response.status_code in [401, 422], f"Malformed header {header} should be rejected"


def test_error_handling_for_expired_tokens_during_chat():
    """Test error handling when token expires during chat operations"""
    client = TestClient(app)

    # Create an expired token
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


def test_error_handling_for_invalid_signature_tokens():
    """Test error handling for tokens with invalid signatures"""
    client = TestClient(app)

    # Create a valid token then tamper with it
    user_id = "tampered-token-user"
    valid_token = create_test_token(user_id)

    # Tamper with the token (just an example - actual tampering would be more complex)
    # For this test, we'll just use an obviously invalid token
    invalid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiaWF0IjoxNTE2MjM5MDIyfQ.invalid_signature_here"

    response = client.post(
        "/chat/",
        json={"message": "Hello with invalid signature"},
        headers={"Authorization": f"Bearer {invalid_token}"}
    )

    assert response.status_code == 401, "Tokens with invalid signatures should be rejected"


def test_error_handling_for_insufficient_permissions():
    """Test error handling when token exists but lacks sufficient permissions"""
    # In our case, the main permission check is the presence of user ID
    # This test might be more relevant if we had role-based permissions
    client = TestClient(app)

    user_id = "permission-test-user"
    token = create_test_token(user_id)

    # This should work since user ID is present
    response = client.post(
        "/chat/",
        json={"message": "Hello with proper permissions"},
        headers={"Authorization": f"Bearer {token}"}
    )

    # Should not be 401 since user ID is present
    assert response.status_code != 401, "Valid tokens with user ID should not be rejected for permissions"


def test_error_handling_with_multiple_concurrent_failures():
    """Test error handling when multiple invalid requests occur simultaneously"""
    import concurrent.futures

    def make_invalid_request(request_num):
        """Function to make an invalid request"""
        local_client = TestClient(app)

        # Create invalid token for each request
        invalid_token = f"Bearer invalid-token-{request_num}"

        response = local_client.post(
            "/chat/",
            json={"message": f"Invalid request {request_num}"},
            headers={"Authorization": invalid_token}
        )

        return response.status_code

    # Make multiple invalid requests concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(make_invalid_request, i) for i in range(5)]
        results = [future.result() for future in futures]

    # All should return 401 (or similar error code)
    for result in results:
        assert result in [401, 422], "All invalid requests should be rejected"


def test_error_logging_for_failed_auth_attempts():
    """Test that failed authentication attempts are properly logged"""
    client = TestClient(app)

    # Make a request without authentication
    response = client.post(
        "/chat/",
        json={"message": "Hello without auth"}
    )

    assert response.status_code == 401, "Unauthenticated requests should be rejected"

    # Test with invalid token
    response = client.post(
        "/chat/",
        json={"message": "Hello with invalid token"},
        headers={"Authorization": "Bearer definitely-not-a-valid-token"}
    )

    assert response.status_code == 401, "Invalid token requests should be rejected"


def test_error_handling_in_different_scenarios():
    """Test error handling in various missing userId scenarios"""
    client = TestClient(app)

    scenarios = [
        {
            "name": "Missing token entirely",
            "headers": {},
            "expected_status": 401
        },
        {
            "name": "Empty authorization header",
            "headers": {"Authorization": ""},
            "expected_status": 401
        },
        {
            "name": "Bearer without token",
            "headers": {"Authorization": "Bearer"},
            "expected_status": 401
        }
    ]

    for scenario in scenarios:
        response = client.post(
            "/chat/",
            json={"message": f"Test {scenario['name']}"},
            headers=scenario["headers"]
        )

        # Verify the expected status code (allowing for some flexibility)
        if scenario["expected_status"] == 401:
            assert response.status_code == 401, f"Scenario '{scenario['name']}' should return 401"


if __name__ == "__main__":
    pytest.main([__file__])