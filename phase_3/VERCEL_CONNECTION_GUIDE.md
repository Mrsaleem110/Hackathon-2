# Vercel Frontend-Backend-Database Connection Guide

This guide addresses the connection issues between Vercel-deployed frontend, backend, and database in the Todo AI Chatbot application.

## Understanding the Architecture

1. **Frontend** (deployed on Vercel): React/Vite application
2. **Backend** (deployed on Vercel): FastAPI application with API endpoints
3. **Database**: NeonDB PostgreSQL database

## Common Vercel Deployment Issues and Solutions

### Issue 1: Environment Variables Not Set Correctly

**Problem**: Your frontend deployed on Vercel doesn't know the URL of your backend.

**Solution**:
1. Go to your Vercel dashboard for the frontend project
2. Navigate to Settings → Environment Variables
3. Update the `VITE_API_BASE_URL` to your backend's Vercel URL:
   ```
   VITE_API_BASE_URL=https://hackathon-2-phase-3-backend.vercel.app
   ```
4. Or whatever your actual backend Vercel URL is

### Issue 2: Backend CORS Configuration

**Problem**: Your backend doesn't allow requests from your frontend's Vercel domain.

**Check**: Your backend CORS configuration in `backend/src/api/main.py` already includes:
```python
allowed_origins.extend([
    "https://*.vercel.app",
    "https://hackathon-2-p-3.vercel.app",  # Specific frontend URL
    "https://hackathon-2-phase-3-backend.vercel.app"  # Specific backend URL
])
```

**Solution**: If your frontend URL is different, add it to the allowed origins:
```python
allowed_origins.extend([
    "https://*.vercel.app",
    "https://your-actual-frontend-domain.vercel.app",  # Replace with your domain
])
```

### Issue 3: Database Connection in Production

**Problem**: Database connection might fail in production due to environment differences.

**Solution**: Ensure your backend Vercel project has the correct database environment variables:
- `DATABASE_URL` or `NEON_DATABASE_URL`
- `BETTER_AUTH_SECRET`
- `OPENAI_API_KEY`

### Issue 4: Authentication Flow Between Services

**Problem**: The hybrid authentication system might have issues in production.

**Solution**: Ensure both services have consistent authentication configuration:
- Same `BETTER_AUTH_SECRET` in both frontend and backend environments
- Proper token validation flow

## Step-by-Step Deployment Configuration

### Step 1: Configure Backend Vercel Project

1. Go to your backend Vercel project dashboard
2. Go to Settings → Environment Variables
3. Add these variables:
   ```
   DATABASE_URL=your_neondb_connection_string
   NEON_DATABASE_URL=your_neondb_connection_string
   BETTER_AUTH_SECRET=your_strong_secret
   OPENAI_API_KEY=your_openai_api_key
   ```

### Step 2: Configure Frontend Vercel Project

1. Go to your frontend Vercel project dashboard
2. Go to Settings → Environment Variables
3. Add these variables:
   ```
   VITE_API_BASE_URL=https://your-backend-project.vercel.app
   NEXT_PUBLIC_OPENAI_API_KEY=your_openai_api_key
   ```

### Step 3: Re-deploy Both Projects

1. Push changes to your git repository
2. Vercel will automatically redeploy both projects with the new environment variables

## Troubleshooting Steps

### 1. Check Browser Console
Open your deployed frontend and check the browser console (F12) for:
- CORS errors
- Network request failures
- Authentication errors

### 2. Check Network Tab
In browser dev tools, check the Network tab for:
- Failed API requests to your backend
- Status codes (400, 401, 500, etc.)

### 3. Test Backend API Directly
Visit your backend Vercel URL directly:
- `https://your-backend-project.vercel.app/`
- `https://your-backend-project.vercel.app/health`

### 4. Verify Environment Variables
Add a temporary debug endpoint to your backend to check if environment variables are properly set:
```python
@app.get("/debug-env")
def debug_env():
    import os
    return {
        "database_url_set": bool(os.getenv("DATABASE_URL")),
        "neon_db_url_set": bool(os.getenv("NEON_DATABASE_URL")),
        "has_auth_secret": bool(os.getenv("BETTER_AUTH_SECRET"))
    }
```

## Common Error Messages and Fixes

### CORS Error
```
Access to fetch at '...' from origin '...' has been blocked by CORS policy
```
→ Fix: Update CORS allowed origins in your backend

### Database Connection Error
```
Connection refused or similar database errors
```
→ Fix: Verify `DATABASE_URL` environment variable in your backend

### 401 Unauthorized
```
Authentication failed
```
→ Fix: Ensure consistent authentication secrets between frontend and backend

## Quick Verification Checklist

- [ ] Frontend `VITE_API_BASE_URL` points to deployed backend URL
- [ ] Backend has CORS configured for frontend's Vercel domain
- [ ] Backend has correct database connection string in environment variables
- [ ] Both projects have consistent `BETTER_AUTH_SECRET`
- [ ] Both projects have been redeployed after environment variable changes
- [ ] API endpoints return successful responses when tested directly

## Testing the Connection

After configuration, test by:
1. Opening your frontend Vercel URL
2. Attempting to log in/register
3. Creating a task
4. Verifying data persists in the database
5. Checking browser console for errors