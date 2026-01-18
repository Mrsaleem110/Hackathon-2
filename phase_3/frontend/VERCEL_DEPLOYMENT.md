# Vercel Deployment Configuration

## Issue
When deploying the frontend to Vercel, the signup page shows a "failed to fetch" error because the frontend is trying to connect to the backend at `http://localhost:8001` instead of the deployed backend URL.

## Root Cause
The `frontend/.env` file contains:
```
VITE_API_BASE_URL=http://localhost:8001
```

This works fine for local development, but when deployed to Vercel, the frontend still tries to connect to localhost, which is not accessible from the deployed frontend.

## Solution

### 1. Update Environment Variable in Vercel Dashboard

When deploying to Vercel, you need to set the `VITE_API_BASE_URL` environment variable in the Vercel project settings:

1. Go to your Vercel dashboard
2. Select your frontend project
3. Go to Settings → Environment Variables
4. Add a new environment variable:
   - Key: `VITE_API_BASE_URL`
   - Value: Your deployed backend URL (e.g., `https://your-backend-project-name.vercel.app`)

### 2. Backend URL for Your Deployed Project

After deploying your backend to Vercel, you'll get a URL in this format:
```
https://your-backend-project-name.vercel.app
```

Use this URL as the value for `VITE_API_BASE_URL` in the frontend deployment.

### 3. Alternative: Relative Path for Same-Domain Deployment

If you deploy both frontend and backend to the same Vercel project or if you have a reverse proxy that serves both from the same domain, you can use a relative path or the same origin:

```
VITE_API_BASE_URL=/api
```

Or if the backend is served from the same domain:

```
VITE_API_BASE_URL=https://your-frontend-domain.com
```

## Steps to Deploy Correctly

1. First, deploy your backend to Vercel and note the generated URL
2. Deploy your frontend to Vercel, but don't finalize yet
3. In the Vercel dashboard, set the `VITE_API_BASE_URL` environment variable to your backend URL
4. Redeploy the frontend

## Testing

After deployment:
- Frontend deployed URL: `https://your-frontend-project.vercel.app`
- Network requests should go to your backend URL, not localhost
- Signup and login should work without "failed to fetch" errors

## Development vs Production

- Local development: `VITE_API_BASE_URL=http://localhost:8001` in `frontend/.env`
- Production deployment: Set `VITE_API_BASE_URL` in Vercel dashboard to your deployed backend URL