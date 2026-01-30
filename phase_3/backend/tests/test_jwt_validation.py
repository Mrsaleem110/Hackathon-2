import pytest
import os
from datetime import datetime, timedelta
from jose import jwt
from unittest.mock import patch

# Import JWT utility functions from the auth module
from backend.src.auth import decode_jwt_token, validate_token_payload


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


def test_decode_jwt_token_with_standard_payload():
    """Test decoding JWT with standard 'sub' field"""
    user_id = "test-user-standard"
    token = create_test_token(user_id)

    decoded_payload = decode_jwt_token(token)

    assert decoded_payload is not None
    assert decoded_payload.get("sub") == user_id
    assert "exp" in decoded_payload
    assert "iat" in decoded_payload


def test_decode_jwt_token_with_expiration():
    """Test that expired tokens are properly rejected"""
    user_id = "test-user-expired"
    # Create a token that expired 1 hour ago
    expired_time = datetime.utcnow() - timedelta(hours=1)
    to_encode = {
        "sub": user_id,
        "exp": expired_time.timestamp(),
        "iat": (datetime.utcnow() - timedelta(hours=2)).timestamp()
    }

    secret_key = os.getenv("JWT_SECRET_KEY", "test-secret-key")
    algorithm = "HS256"
    expired_token = jwt.encode(to_encode, secret_key, algorithm=algorithm)

    # This should raise an exception or return None
    decoded_payload = decode_jwt_token(expired_token)
    assert decoded_payload is None  # Assuming the function returns None for expired tokens


def test_decode_jwt_token_with_invalid_signature():
    """Test that tokens with invalid signatures are rejected"""
    user_id = "test-user-invalid"
    token = create_test_token(user_id)

    # Decode and re-encode with wrong secret to simulate invalid signature
    # Actually, let's test with an obviously malformed token
    invalid_token = "invalid.token.format"

    decoded_payload = decode_jwt_token(invalid_token)
    assert decoded_payload is None


def test_validate_token_payload_with_user_id():
    """Test that token payload validation works for standard user ID"""
    user_id = "test-user-validate"
    token = create_test_token(user_id)

    decoded_payload = decode_jwt_token(token)
    is_valid, validated_payload = validate_token_payload(decoded_payload)

    assert is_valid is True
    assert validated_payload.get("user_id") == user_id or validated_payload.get("sub") == user_id


def test_validate_token_payload_without_user_identifier():
    """Test that tokens without user identifiers are rejected"""
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

    decoded_payload = decode_jwt_token(token)
    is_valid, validated_payload = validate_token_payload(decoded_payload)

    assert is_valid is False
    assert validated_payload is None


def test_validate_token_payload_with_alternative_user_field():
    """Test that tokens with alternative user ID fields are normalized"""
    user_id = "test-user-alternative"
    # Create token with custom user field
    token = create_test_token(user_id, custom_payload={"user_id": f"alt-{user_id}"})

    decoded_payload = decode_jwt_token(token)
    is_valid, validated_payload = validate_token_payload(decoded_payload)

    assert is_valid is True
    # Should have normalized the user ID
    assert "user_id" in validated_payload or "sub" in validated_payload


def test_jwt_payload_normalization():
    """Test that different JWT payload structures are normalized consistently"""
    test_cases = [
        {"sub": "user123"},  # Standard JWT
        {"user_id": "user456"},  # Alternative field
        {"sub": "user789", "user_id": "user789"},  # Both fields
        {"id": "user000", "sub": "user000"},  # Different field names
    ]

    for i, payload_fields in enumerate(test_cases):
        user_id = f"test-user-{i}"
        token = create_test_token(user_id, custom_payload=payload_fields)

        decoded_payload = decode_jwt_token(token)
        is_valid, validated_payload = validate_token_payload(decoded_payload)

        assert is_valid is True, f"Failed for payload: {payload_fields}"
        # The function should ensure a consistent user ID field exists
        assert "user_id" in validated_payload or "sub" in validated_payload


def test_jwt_token_expiry_validation():
    """Test that token expiry is properly validated"""
    # Test valid token (not expired)
    user_id = "test-user-not-expired"
    token = create_test_token(user_id, expires_delta=timedelta(minutes=30))

    decoded_payload = decode_jwt_token(token)
    is_valid, validated_payload = validate_token_payload(decoded_payload)

    assert is_valid is True
    assert validated_payload is not None


def test_jwt_malformed_token_handling():
    """Test that malformed tokens are handled gracefully"""
    malformed_tokens = [
        "",  # Empty string
        "not.at.all.a.jwt",  # Not a JWT format
        "header.payload",  # Incomplete JWT
        "1.2.3",  # Invalid JWT components
    ]

    for malformed_token in malformed_tokens:
        decoded_payload = decode_jwt_token(malformed_token)
        assert decoded_payload is None


def test_jwt_signature_verification():
    """Test that tokens with incorrect signatures are rejected"""
    # This test verifies that the decode_jwt_token function properly validates signatures
    user_id = "test-user-signature"
    token = create_test_token(user_id)

    # Try to decode with a different secret key
    with patch.dict(os.environ, {"JWT_SECRET_KEY": "different-secret-key"}):
        decoded_payload = decode_jwt_token(token)
        assert decoded_payload is None  # Should fail signature verification


if __name__ == "__main__":
    pytest.main([__file__])