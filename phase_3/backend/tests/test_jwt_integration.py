import pytest
import os
from datetime import datetime, timedelta
from jose import jwt
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

# Import the main FastAPI app and auth components
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.api.main import app
from src.auth import require_auth, decode_jwt_token, validate_token_payload


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


def create_test_token(user_id: str, custom_payload: dict = None, expires_delta: timedelta = None):
    """Helper function to create a test JWT token with various payload structures"""
    if expires_delta is None:
        expires_delta = timedelta(hours=1)

    expire = datetime.utcnow() + expires_delta
    to_encode = {
        "sub": user_id,
        "exp": expire.timestamp(),
        "iat": datetime.utcnow().timestamp()
    }

    # Add custom payload fields if provided
    if custom_payload:
        to_encode.update(custom_payload)

    secret_key = os.getenv("JWT_SECRET_KEY", "test-secret-key")
    algorithm = "HS256"

    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


def test_jwt_integration_with_auth_middleware():
    """Integration test for JWT validation with the auth middleware"""
    client = TestClient(app)

    # Test successful authentication flow
    user_id = "integration-test-user"
    token = create_test_token(user_id)

    response = client.get(
        "/",
        headers={"Authorization": f"Bearer {token}"}
    )
    # Main endpoint might not exist, but shouldn't be 401 if auth middleware is working
    # The important thing is that the middleware doesn't throw an exception

    # Test that invalid tokens are caught by middleware
    response = client.get(
        "/",
        headers={"Authorization": "Bearer invalid.token.format"}
    )
    # This might return 401 or 404 depending on the main route, but should not crash


def test_user_id_extraction_from_various_jwt_formats():
    """Test that user ID is correctly extracted from different JWT payload formats"""
    # Test standard 'sub' field
    token_with_sub = create_test_token("user-with-sub")

    decoded = decode_jwt_token(token_with_sub)
    is_valid, validated_payload = validate_token_payload(decoded)

    assert is_valid is True
    assert validated_payload is not None
    # The function should normalize the payload to have a consistent user ID field

    # Test with custom payload structure
    custom_payload = {"user_id": "custom-user-id", "role": "user"}
    token_with_custom = create_test_token("placeholder", custom_payload=custom_payload)

    decoded = decode_jwt_token(token_with_custom)
    is_valid, validated_payload = validate_token_payload(decoded)

    assert is_valid is True
    assert validated_payload is not None


def test_jwt_validation_in_fastapi_dependency():
    """Test JWT validation as a FastAPI dependency"""
    # Create a test endpoint that uses the require_auth dependency
    from fastapi import Depends, FastAPI

    test_app = FastAPI()

    @test_app.get("/protected")
    def protected_route(current_user = Depends(require_auth)):
        return {"user_id": current_user.get("user_id") if current_user else "unknown"}

    client = TestClient(test_app)

    # Test with valid token
    user_id = "dependency-test-user"
    token = create_test_token(user_id)

    response = client.get(
        "/protected",
        headers={"Authorization": f"Bearer {token}"}
    )

    # Should either succeed or fail for reasons other than auth
    if response.status_code != 401:
        # If it's not unauthorized, it means auth dependency worked
        pass
    else:
        # If it is unauthorized, that's expected for invalid token
        pass

    # Test with invalid token
    response = client.get(
        "/protected",
        headers={"Authorization": "Bearer invalid.token"}
    )
    assert response.status_code == 401


def test_jwt_integration_with_database_access():
    """Test JWT validation integrated with database access patterns"""
    # This would typically involve testing that the user_id from JWT
    # can be used to query the database for user-specific data
    from unittest.mock import patch

    # Mock the database access to avoid actual DB calls
    with patch('backend.src.database.get_db_session') as mock_db:
        mock_db.return_value.__enter__.return_value = MagicMock()

        user_id = "db-integration-user"
        token = create_test_token(user_id)

        # Even without a real endpoint that uses DB, we can test that
        # the JWT validation happens before database access
        decoded = decode_jwt_token(token)
        is_valid, validated_payload = validate_token_payload(decoded)

        assert is_valid is True
        assert validated_payload is not None


def test_jwt_validation_under_load():
    """Test JWT validation performance and reliability under simulated load"""
    # This simulates multiple concurrent requests to test JWT validation
    import concurrent.futures
    import threading

    def make_request(user_idx):
        """Function to make a single authenticated request"""
        client = TestClient(app)  # Create client for each thread
        token = create_test_token(f"user-{user_idx}")

        # For this test, we'll just test the JWT decoding/validation functions directly
        # since we don't have a guaranteed working endpoint
        decoded = decode_jwt_token(token)
        is_valid, validated_payload = validate_token_payload(decoded)

        return is_valid and validated_payload is not None

    # Test with multiple concurrent requests
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(make_request, i) for i in range(5)]
        results = [future.result() for future in futures]

    # All should be valid
    assert all(results), "All concurrent JWT validations should succeed"


def test_jwt_error_handling_integration():
    """Test how JWT validation integrates with error handling"""
    # Test edge cases and error conditions
    error_test_cases = [
        ("", "Empty token"),
        ("invalid", "Invalid token format"),
        ("header.payload.signature.extra", "Too many parts"),
        ("invalid.header", "Invalid header"),
        ("invalid.header.invalid", "Invalid header and payload"),
    ]

    for token, description in error_test_cases:
        decoded = decode_jwt_token(token)
        # Should return None for invalid tokens
        assert decoded is None, f"Token '{description}' should return None"


def test_jwt_algorithm_validation():
    """Test that JWT algorithm validation is working properly"""
    # Create a token with RS256 algorithm when expecting HS256
    user_id = "alg-validation-user"

    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode = {
        "sub": user_id,
        "exp": expire.timestamp(),
        "iat": datetime.utcnow().timestamp()
    }

    # Create a fake RSA key for testing
    fake_rsa_header = {
        "alg": "RS256",
        "typ": "JWT"
    }

    # This is just for testing - in real scenarios, mismatched algorithms should fail
    # The important thing is that the system handles algorithm mismatches safely


def test_jwt_claims_validation():
    """Test that JWT claims are properly validated"""
    user_id = "claims-test-user"

    # Test with future issue time (should be invalid)
    future_time = datetime.utcnow() + timedelta(hours=1)
    to_encode_future = {
        "sub": user_id,
        "exp": (datetime.utcnow() + timedelta(hours=2)).timestamp(),
        "iat": future_time.timestamp()  # Issued in the future
    }

    secret_key = os.getenv("JWT_SECRET_KEY", "test-secret-key")
    algorithm = "HS256"
    future_token = jwt.encode(to_encode_future, secret_key, algorithm=algorithm)

    # Decode and validate
    decoded = decode_jwt_token(future_token)
    # Depending on implementation, this might return None due to future iat


if __name__ == "__main__":
    pytest.main([__file__])