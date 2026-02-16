# CORS Configuration Fix for Your Vercel Deployment

## Current Issue Analysis:
- Frontend: https://hackathon-2-p-3-frontend.vercel.app
- Backend: https://hackathon-2-p-3-backend.vercel.app
- The backend is not properly configured to accept requests from your frontend domain

## Solution Steps:

### 1. Update Backend Environment Variables in Vercel Dashboard:
Go to your backend project (hackathon-2-p-3-backend) in Vercel dashboard and set:

```
CORS_ORIGINS=https://hackathon-2-p-3-frontend.vercel.app,https://*.vercel.app
FRONTEND_URL=https://hackathon-2-p-3-frontend.vercel.app
BETTER_AUTH_URL=https://hackathon-2-p-3-frontend.vercel.app
```

### 2. Update your backend's CORS configuration
Look for your CORS setup in backend/src/api/main.py and ensure it includes your specific domains:

```python
# In your main.py, make sure CORS is configured like this:
cors_origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:3000",
    "https://hackathon-2-p-3-frontend.vercel.app",  # Your specific frontend
    "https://hackathon-2-p-3-backend.vercel.app",   # Your backend domain
    "https://*.vercel.app",  # Wildcard for Vercel
]
```

### 3. Additional Backend Environment Variables Needed:
Also set these in your backend Vercel environment:

```
BETTER_AUTH_SECRET=your_unique_secret_key
SECRET_KEY=your_unique_jwt_secret_key
DATABASE_URL=your_database_connection_string
```

### 4. Redeploy Your Backend
After updating these environment variables, redeploy your backend project.

### 5. Verify Backend Health
Test if your backend is working:
- Visit: https://hackathon-2-p-3-backend.vercel.app/health
- This should return a healthy response
- Visit: https://hackathon-2-p-3-backend.vercel.app/debug/test
- This should confirm the backend is running

### 6. Test CORS Configuration
Try this command to test if CORS is properly configured:
```bash
curl -H "Origin: https://hackathon-2-p-3-frontend.vercel.app" \
     -H "Access-Control-Request-Method: POST" \
     -H "Access-Control-Request-Headers: X-Requested-With" \
     -X OPTIONS https://hackathon-2-p-3-backend.vercel.app/auth/login \
     -i
```

The response should include:
```
Access-Control-Allow-Origin: https://hackathon-2-p-3-frontend.vercel.app
```

This specific configuration will fix the cross-origin request issue you're experiencing.