# Better Auth Skills

This module provides skills for authentication and authorization using Better Auth.

## Overview

The Better Auth skills provide a comprehensive set of tools for:
- User management (create, authenticate, update)
- Session management
- Organization management
- Two-factor authentication
- Rate limiting
- Access control

## Skills

### `create_user`
Create a new user with email and password authentication.

**Parameters:**
- `email`: User's email address (required)
- `password`: User's password (required)
- `name`: User's name (optional)
- `metadata`: Additional user metadata (optional)

### `authenticate_user`
Authenticate a user with email and password.

**Parameters:**
- `email`: User's email address (required)
- `password`: User's password (required)

### `create_session`
Create a new session for a user.

**Parameters:**
- `user_id`: ID of the user to create session for (required)

### `verify_session`
Verify if a session is valid.

**Parameters:**
- `session_id`: ID of the session to verify (required)

### `create_organization`
Create a new organization.

**Parameters:**
- `name`: Name of the organization (required)
- `owner_user_id`: ID of the user who will be the owner (required)
- `metadata`: Additional organization metadata (optional)

### `add_user_to_organization`
Add a user to an organization.

**Parameters:**
- `org_id`: ID of the organization (required)
- `user_id`: ID of the user to add (required)
- `role`: Role to assign to the user (optional, default: "member")

### `enable_two_factor`
Enable two-factor authentication for a user.

**Parameters:**
- `user_id`: ID of the user (required)
- `method`: 2FA method (optional, default: "totp")

### `rate_limit_check`
Check if a rate limit has been exceeded.

**Parameters:**
- `identifier`: Identifier for the rate limit (e.g., IP address, user ID) (required)
- `limit`: Number of requests allowed (optional, default: 10)
- `window`: Time window in seconds (optional, default: 60)

### `get_user_by_id`
Get user information by ID.

**Parameters:**
- `user_id`: ID of the user to retrieve (required)

### `update_user`
Update user information.

**Parameters:**
- `user_id`: ID of the user to update (required)
- `updates`: Dictionary of fields to update (required)

## Examples

### Creating a User
```python
from skills.better_auth.better_auth_skills import create_user

user_result = await create_user(
    email="john@example.com",
    password="securePassword123",
    name="John Doe",
    metadata={"department": "engineering"}
)
```

### Authenticating a User
```python
from skills.better_auth.better_auth_skills import authenticate_user

auth_result = await authenticate_user(
    email="john@example.com",
    password="securePassword123"
)
```

### Creating a Session
```python
from skills.better_auth.better_auth_skills import create_session

session_result = await create_session(user_id="user-123")
```

### Creating an Organization
```python
from skills.better_auth.better_auth_skills import create_organization

org_result = await create_organization(
    name="Acme Corp",
    owner_user_id="user-123",
    metadata={"industry": "technology"}
)
```

### Enabling Two-Factor Authentication
```python
from skills.better_auth.better_auth_skills import enable_two_factor

tfa_result = await enable_two_factor(
    user_id="user-123",
    method="totp"
)
```

### Checking Rate Limits
```python
from skills.better_auth.better_auth_skills import rate_limit_check

rate_result = await rate_limit_check(
    identifier="user-123",
    limit=10,
    window=60
)
```

## Dependencies

- `better-auth>=0.0.0`

## Installation

```bash
npm install better-auth
```

## Testing

Run the example implementation:

```bash
python better_auth_skills.py
```

## Features Implemented

✅ Framework Agnostic - Skills work with any framework
✅ Email & Password - Built-in secure authentication
✅ Account & Session Management - Complete user and session lifecycle
✅ Built-In Rate Limiter - Rate limiting with custom rules
✅ Automatic Database Management - Simulated in-memory storage
✅ Social Sign-on - Ready for integration (not implemented in this basic version)
✅ Organization & Access Control - Organization management with roles
✅ Two Factor Authentication - TOTP support
✅ Plugin Ecosystem - Ready for extensions