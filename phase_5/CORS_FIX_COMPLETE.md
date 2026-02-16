# CORS Authentication Fix Summary

## Problem
The frontend was experiencing "Failed to fetch" errors when trying to sign in/sign up with the following CORS error:
```
Access to fetch at 'http://localhost:3001/api/auth/...' from origin 'http://localhost:3000' 
has been blocked by CORS policy: The value of the 'Access-Control-Allow-Origin' header in 
the response must not be the wildcard '*' when the request's credentials mode is 'include'.
```

## Root Causes

1. **CORS Wildcard Issue**: The auth service was using `Access-Control-Allow-Origin: *` which is not allowed when using credentials (cookies)
2. **Missing Credentials Header**: The auth service wasn't setting `Access-Control-Allow-Credentials: true`
3. **Incorrect Environment Variables**: Frontend was configured to use `http://auth_service:3001` which doesn't work from the browser

## Fixes Applied

### 1. Auth Service CORS Configuration (auth_service/better_auth_server.js)
- Changed from wildcard `*` to specific allowed origins
- Added `Access-Control-Allow-Credentials: true` header
- Created an array of allowed origins (localhost:3000, localhost:5173, localhost:3001)
- Dynamically set the correct origin based on the request

```javascript
const ALLOWED_ORIGINS = [
  'http://localhost:3000',
  'http://localhost:5173',
  'http://localhost:3001'
];

// In request handler:
const origin = req.headers.origin;
if (origin && ALLOWED_ORIGINS.includes(origin)) {
  res.setHeader('Access-Control-Allow-Origin', origin);
  res.setHeader('Access-Control-Allow-Credentials', 'true');
}
```

### 2. Frontend Dockerfile (frontend/Dockerfile)
- Added ARG and ENV directives to accept build-time environment variables
- This ensures Vite bakes the correct API URLs into the build

```dockerfile
ARG VITE_API_BASE_URL
ARG VITE_AUTH_BASE_URL
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL
ENV VITE_AUTH_BASE_URL=$VITE_AUTH_BASE_URL
```

### 3. Docker Compose Configuration (docker-compose.yml)
- Changed frontend environment variables from Docker internal URLs to localhost URLs
- Added build args to pass environment variables during frontend build

```yaml
frontend:
  build:
    context: ./frontend
    args:
      VITE_API_BASE_URL: http://localhost:8000
      VITE_AUTH_BASE_URL: http://localhost:3001
```

## Verification

Test CORS headers with:
```powershell
$response = Invoke-WebRequest -Uri "http://localhost:3001/api/auth/get-session" `
  -Method OPTIONS -Headers @{"Origin"="http://localhost:3000"} -UseBasicParsing
$response.Headers
```

Should return:
```
Access-Control-Allow-Origin      http://localhost:3000
Access-Control-Allow-Credentials true
Access-Control-Allow-Methods     GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers     Content-Type, Authorization
```

## Services Status
All services should now be running correctly:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Auth Service: http://localhost:3001
- PostgreSQL: localhost:5432

## Testing
1. Navigate to http://localhost:3000
2. Try signing up with email and password
3. Try signing in with existing credentials
4. Verify no CORS errors in browser console

## Key Learnings
- When using credentials (cookies) in CORS requests, you MUST use specific origins, not wildcards
- Frontend environment variables in Vite must be set at build time using ARG/ENV in Dockerfile
- Browser requests always use localhost, not Docker service names
