# Authentication Issues Troubleshooting Guide

## Issue 1: "Invalid credentials" during Sign In

### Root Causes:
1. **Domain mismatch**: Your authentication system expects requests from a specific domain, but receives them from Vercel's deployed URL
2. **Cookie/Session misconfiguration**: Authentication cookies aren't being shared properly between frontend and backend
3. **CORS misconfiguration**: Cross-origin requests aren't properly configured
4. **Environment variables mismatch**: Different secrets between frontend and backend deployments

### Solutions:
1. **Update CORS settings in your backend** to include your frontend's Vercel URL
2. **Ensure consistent environment variables** across both deployments
3. **Configure authentication system** (Better Auth or JWT) to work across domains
4. **Check that your authentication endpoint URLs** are pointing to the correct deployed backend

## Issue 2: "Failed to load dashboard data. Backend may be unreachable" during Sign Up

### Root Causes:
1. **Backend API endpoint misconfiguration**: Frontend is trying to reach backend at wrong URL
2. **Network connectivity issues**: Vercel deployments can't communicate properly
3. **Authentication token not properly stored/used**: Missing authentication for dashboard requests
4. **Backend health issues**: The deployed backend might not be functioning correctly

### Solutions:
1. **Verify your API base URL** in frontend environment variables points to your deployed backend
2. **Check backend health endpoint**: Access `https://your-backend.vercel.app/health` to confirm it's running
3. **Ensure authentication tokens** are properly stored and sent with dashboard requests
4. **Review CORS configuration** to allow communication between frontend and backend domains

## Step-by-Step Fix Guide

### 1. Check Backend Health
Visit: `https://your-backend-project-name.vercel.app/health`
Expected response: `{"status": "healthy", ...}`

### 2. Verify Environment Variables
Frontend `.env` should have:
```
VITE_API_BASE_URL=https://your-backend-project-name.vercel.app
VITE_CHATKIT_DOMAIN_KEY=your_domain_key
```

Backend `.env` should have:
```
BETTER_AUTH_URL=https://your-frontend-project-name.vercel.app
BETTER_AUTH_SECRET=your_shared_secret
SECRET_KEY=your_jwt_secret
```

### 3. Check CORS Configuration
Your backend should allow requests from your frontend domain:
- Frontend domain: `https://your-frontend-project-name.vercel.app`
- Backend domain: `https://your-backend-project-name.vercel.app`

### 4. Verify Authentication Flow
1. Sign up request should go to: `POST https://your-backend-project-name.vercel.app/auth/register`
2. Login request should go to: `POST https://your-backend-project-name.vercel.app/auth/login`
3. Dashboard request should include auth token: `GET https://your-backend-project-name.vercel.app/dashboard/data`

## Common Fixes for Vercel Deployments

### Frontend Environment Variables (in Vercel dashboard):
- `VITE_API_BASE_URL`: Set to your deployed backend URL
- `VITE_CHATKIT_DOMAIN_KEY`: Your OpenAI ChatKit domain key

### Backend Environment Variables (in Vercel dashboard):
- `BETTER_AUTH_URL`: Set to your deployed frontend URL
- `BETTER_AUTH_SECRET`: Same secret used in frontend
- `SECRET_KEY`: JWT secret for token signing
- `CORS_ORIGINS`: Comma-separated list of allowed origins (your frontend URL)

## Testing Steps
1. Test backend health: `curl https://your-backend-project-name.vercel.app/health`
2. Test backend auth routes: `curl https://your-backend-project-name.vercel.app/auth/test`
3. Check browser network tab for failed requests
4. Verify that authentication tokens are stored in browser after login

## Debugging Commands
Run these to diagnose issues:
```bash
# Test backend connectivity
curl -X GET https://your-backend-project-name.vercel.app/health

# Test auth routes
curl -X GET https://your-backend-project-name.vercel.app/debug/routes

# Test CORS configuration
curl -H "Origin: https://your-frontend-project-name.vercel.app" \
     -H "Access-Control-Request-Method: POST" \
     -H "Access-Control-Request-Headers: X-Requested-With" \
     -X OPTIONS https://your-backend-project-name.vercel.app/auth/login \
     -i
```