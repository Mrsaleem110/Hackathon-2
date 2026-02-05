# CORS and Authentication Fix Guide

## Current Issue Analysis:
- Frontend: https://hackathon-2-p-3-frontend.vercel.app
- Backend: https://hackathon-2-p-3-backend.vercel.app
- Cross-origin request is failing due to CORS misconfiguration
- Login request is failing with server error

## Solution Steps:

### 1. Verify Backend Environment Variables in Vercel Dashboard:
Make sure these are set in your backend project in Vercel:

```
CORS_ORIGINS=https://hackathon-2-p-3-frontend.vercel.app,https://*.vercel.app
FRONTEND_URL=https://hackathon-2-p-3-frontend.vercel.app
BETTER_AUTH_URL=https://hackathon-2-p-3-frontend.vercel.app
BETTER_AUTH_SECRET=your_unique_secret_key
SECRET_KEY=your_unique_jwt_secret_key
DATABASE_URL=your_database_connection_string
NEON_DATABASE_URL=your_neon_database_connection_string (if using Neon)
```

### 2. Check Backend Health:
First, verify if your backend is running properly:
- Visit: https://hackathon-2-p-3-backend.vercel.app/health
- This should return: {"status": "healthy", ...}

### 3. Test Backend Endpoints:
- Visit: https://hackathon-2-p-3-backend.vercel.app/debug/test
- Visit: https://hackathon-2-p-3-backend.vercel.app/auth/test

### 4. If Backend is Working, Test CORS Configuration:
Try this command to test if CORS is properly configured:
```bash
curl -H "Origin: https://hackathon-2-p-3-frontend.vercel.app" \
     -H "Access-Control-Request-Method: POST" \
     -H "Access-Control-Request-Headers: Content-Type, Authorization" \
     -X OPTIONS https://hackathon-2-p-3-backend.vercel.app/auth/login \
     -i
```

The response should include:
```
Access-Control-Allow-Origin: https://hackathon-2-p-3-frontend.vercel.app
```

### 5. If CORS is Still Not Working:
The issue might be that the CORS configuration needs to be enhanced in your backend. Make sure your backend is redeployed after setting the environment variables.