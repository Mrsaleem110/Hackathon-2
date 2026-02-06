# Vercel Authentication Fix Guide

This guide addresses common authentication issues when deploying frontend and backend to Vercel.

## Common Authentication Issues in Vercel Deployments

### 1. Invalid Credentials Error During Sign In

**Root Cause**:
- Domain mismatch in authentication system
- Incorrect CORS configuration
- Environment variable discrepancies between frontend and backend

**Solutions**:

#### A. Update CORS Configuration in Backend

Make sure your backend allows requests from your frontend domain:

```python
# In your main.py or wherever CORS is configured
frontend_url = os.getenv("FRONTEND_URL", "https://your-frontend-project.vercel.app")

cors_origins = [
    "http://localhost:5173",  # Local development
    "http://localhost:3000",  # Local development
    frontend_url,             # Your deployed frontend
    f"https://{os.getenv('VERCEL_PROJECT_NAME')}-frontend.vercel.app",  # Dynamic Vercel URL
    f"https://{os.getenv('VERCEL_PROJECT_NAME')}-backend.vercel.app",   # Backend domain
    "https://*.vercel.app",   # Wildcard for Vercel previews
]
```

#### B. Verify Environment Variables

**Frontend (Vercel Environment Variables)**:
```
VITE_API_BASE_URL=https://your-backend-project.vercel.app
VITE_CHATKIT_DOMAIN_KEY=your_openai_domain_key
```

**Backend (Vercel Environment Variables)**:
```
BETTER_AUTH_URL=https://your-frontend-project.vercel.app
BETTER_AUTH_SECRET=your_shared_secret_key
SECRET_KEY=your_jwt_secret_key
FRONTEND_URL=https://your-frontend-project.vercel.app
```

### 2. "Failed to load dashboard data. Backend may be unreachable" During Sign Up

**Root Cause**:
- API base URL mismatch in frontend
- Network connectivity issues between Vercel deployments
- Authentication token not properly stored or sent

**Solutions**:

#### A. Fix Frontend API Base URL

In your frontend's `.env.production` or Vercel environment:
```
VITE_API_BASE_URL=https://your-backend-project.vercel.app
```

#### B. Verify Backend Endpoints

Test your backend endpoints directly:
```bash
curl -X GET https://your-backend-project.vercel.app/health
curl -X GET https://your-backend-project.vercel.app/debug/routes
```

#### C. Check Authentication Token Handling

Ensure your frontend properly stores and sends authentication tokens:
- After successful login, verify that JWT tokens or session cookies are stored
- Check that subsequent requests include proper authorization headers
- Verify that the token is sent with dashboard requests

## Step-by-Step Fix Process

### Step 1: Verify Both Deployments Are Active
- Frontend: `https://your-frontend-project.vercel.app`
- Backend: `https://your-backend-project.vercel.app`

### Step 2: Check Backend Health
Visit: `https://your-backend-project.vercel.app/health`
Expected: `{"status": "healthy", ...}`

### Step 3: Update Vercel Environment Variables

For **Frontend** in Vercel dashboard:
1. Go to your frontend project in Vercel
2. Navigate to Settings → Environment Variables
3. Add:
   - Key: `VITE_API_BASE_URL`, Value: `https://your-backend-project.vercel.app`
   - Key: `VITE_CHATKIT_DOMAIN_KEY`, Value: your OpenAI domain key

For **Backend** in Vercel dashboard:
1. Go to your backend project in Vercel
2. Navigate to Settings → Environment Variables
3. Add:
   - Key: `BETTER_AUTH_URL`, Value: `https://your-frontend-project.vercel.app`
   - Key: `BETTER_AUTH_SECRET`, Value: a strong secret key (same as frontend)
   - Key: `SECRET_KEY`, Value: a strong JWT secret key
   - Key: `FRONTEND_URL`, Value: `https://your-frontend-project.vercel.app`
   - Key: `CORS_ORIGINS`, Value: `https://your-frontend-project.vercel.app,https://*.vercel.app`

### Step 4: Redeploy Both Projects

After updating environment variables:
1. Trigger a new deployment for both frontend and backend
2. Wait for both deployments to complete successfully

### Step 5: Test Authentication Flow

1. Visit your frontend URL
2. Try signing up with a new account
3. Try signing in with the new account
4. Verify that dashboard loads after login

## Debugging Commands

Run these commands to diagnose issues:

```bash
# Test backend connectivity
curl -X GET https://your-backend-project.vercel.app/health

# Test auth endpoints
curl -X POST https://your-backend-project.vercel.app/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass123"}'

# Test CORS preflight
curl -X OPTIONS https://your-backend-project.vercel.app/auth/login \
  -H "Origin: https://your-frontend-project.vercel.app" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type" \
  -i
```

## Common Gotchas

1. **Secret Keys**: Make sure `BETTER_AUTH_SECRET` and `SECRET_KEY` are the same between frontend and backend
2. **HTTPS**: Vercel enforces HTTPS, ensure all URLs use https://
3. **Domain Allowlist**: If using OpenAI ChatKit, ensure your domain is added to the allowlist
4. **Cache Issues**: Clear browser cache after redeployment
5. **Session Storage**: Check if authentication tokens are being stored in localStorage vs cookies appropriately