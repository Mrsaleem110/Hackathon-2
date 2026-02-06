# Data Model: Authentication System

## User Entity

### Core Attributes
- **id**: string (primary identifier, UUID format)
- **email**: string (unique, validated email format)
- **name**: string (display name, optional)
- **created_at**: datetime (timestamp of account creation)
- **updated_at**: datetime (timestamp of last update)

### Authentication Attributes
- **hashed_password**: string (bcrypt hash of user password)
- **is_active**: boolean (account status, defaults to true)
- **last_login**: datetime (timestamp of last successful login)

## Session Entity

### JWT Token Structure
- **sub**: string (subject - user ID)
- **exp**: integer (expiration timestamp)
- **iat**: integer (issued at timestamp)
- **user_id**: string (reference to User.id)
- **email**: string (user email for verification)
- **name**: string (user name for context)

## Authentication Request Models

### LoginRequest
- **email**: string (required, validated email format)
- **password**: string (required, minimum 8 characters)

### RegisterRequest
- **email**: string (required, validated email format)
- **password**: string (required, minimum 8 characters)
- **name**: string (optional, display name)

## Authentication Response Models

### AuthSuccessResponse
- **access_token**: string (JWT token)
- **token_type**: string (always "bearer")
- **user**: User object (contains id, email, name)

### AuthErrorResponse
- **detail**: string (human-readable error message)
- **error_code**: string (machine-readable error code)

## Chat Request Model

### ChatRequest
- **message**: string (required, user message content)
- **conversation_id**: string (optional, existing conversation identifier)
- **user_id**: string (derived from JWT token, validated server-side)

## Security Constraints

### Token Validation
- JWT tokens must be signed with server's secret key
- Tokens must include valid expiration (exp) claim
- Token user_id must match database user record
- Expired tokens must be rejected

### Rate Limiting
- Maximum 100 requests per hour per user
- IP-based rate limiting for unauthenticated requests
- Account lockout after 5 failed login attempts

### Session Management
- Sessions expire after 24 hours of inactivity
- Refresh tokens invalidate after 7 days
- Concurrent sessions limited to 5 per user