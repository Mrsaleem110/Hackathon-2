# Quickstart Guide: Authentication System

## Setup Authentication

### Environment Variables
```bash
# Backend (backend/.env)
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
DATABASE_URL=postgresql+asyncpg://username:password@host:port/dbname
NEON_DATABASE_URL=your-neon-database-url
```

### Frontend Configuration
```bash
# Frontend (frontend/.env)
VITE_API_BASE_URL=https://your-backend-url.com
```

## Authentication Flow

### 1. User Registration
```javascript
// POST /auth/register
const response = await fetch('/auth/register', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'securePassword123',
    name: 'John Doe'
  })
});

// Expected response:
{
  "access_token": "jwt_token_here",
  "token_type": "bearer",
  "user": {
    "id": "user_xxxxxxxxxxxx",
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

### 2. User Login
```javascript
// POST /auth/login
const response = await fetch('/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'securePassword123'
  })
});
```

### 3. Token Verification (Backend Middleware)
```python
from fastapi import Depends, HTTPException
from src.auth import require_auth

# Apply to protected endpoints
@router.post("/chat")
async def send_message(
    message_data: dict,
    current_user: User = Depends(require_auth())
):
    # current_user.id is guaranteed to exist
    # Process chat message with verified user context
```

### 4. Frontend Auth Verification
```javascript
// In AuthContext.jsx
const userId = user?.id; // This is now guaranteed to exist when authenticated

// In ChatInterface.jsx
if (!userId) {
  // Show appropriate error/loading state
  return <div>Verifying authentication...</div>;
}
```

## Protected Routes Implementation

### Route Guard (App.jsx)
```jsx
<Route path="/chat" element={
  user && user.id ?
    <ProtectedLayout user={user}>
      <ChatInterface userId={user.id} />
    </ProtectedLayout>
  :
  <Navigate to="/login" replace />
} />
```

## JWT Token Structure

### Claims
- `sub`: User ID (string)
- `exp`: Expiration timestamp (integer)
- `iat`: Issued at timestamp (integer)
- `user_id`: User identifier (string)
- `email`: User email (string)
- `name`: User display name (string)

### Verification
```python
def verify_token(token: str) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception

    user = get_user(user_id=token_data.user_id)
    if user is None:
        raise credentials_exception
    return user
```

## Error Handling

### Missing User ID
- Frontend: Redirect to login or show authentication error
- Backend: Return 401 Unauthorized for protected endpoints
- Logging: Log authentication failures for monitoring

### Token Expiry
- Frontend: Automatically redirect to login
- Backend: Reject expired tokens with clear error message
- Refresh: Implement token refresh if needed

## Security Best Practices

### Password Requirements
- Minimum 8 characters
- Include uppercase, lowercase, numbers, and special characters
- Never store plaintext passwords

### Token Security
- Use strong secret keys (32+ characters)
- Set appropriate expiration times
- Rotate secrets periodically
- Never expose tokens in client-side logs

### Session Management
- Invalidate tokens on logout
- Implement concurrent session limits
- Monitor for suspicious activity
- Log authentication events