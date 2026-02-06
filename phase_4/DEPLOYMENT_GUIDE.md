# Deployment Guide

## Deploying to Vercel

This application consists of two parts that need to be deployed separately:
1. Backend API (FastAPI application)
2. Frontend (React/Vite application)

## Step-by-Step Deployment Process

### 1. Deploy the Backend First
- Deploy the backend to Vercel using the `backend/` directory
- Set the required environment variables in Vercel dashboard:
  - `DATABASE_URL`
  - `OPENAI_API_KEY`
  - `NEON_DATABASE_URL`
  - `BETTER_AUTH_SECRET`
  - `BETTER_AUTH_URL` (set to your frontend URL when deployed)
  - `FRONTEND_URL` (optional, your frontend deployment URL)

Note the backend URL after deployment (e.g., `https://your-backend-project.vercel.app`)

### 2. Deploy the Frontend
- Deploy the frontend to Vercel using the root directory or `frontend/` directory
- Set the `VITE_API_BASE_URL` environment variable in Vercel dashboard to your backend URL
  - Key: `VITE_API_BASE_URL`
  - Value: Your backend deployment URL (e.g., `https://your-backend-project.vercel.app`)

## Troubleshooting Common Issues

### "Failed to fetch" Error
- **Cause**: Frontend trying to connect to localhost instead of deployed backend
- **Solution**: Ensure `VITE_API_BASE_URL` is set correctly in Vercel dashboard

### CORS Errors
- **Cause**: Backend not allowing requests from frontend domain
- **Solution**: Ensure the backend allows requests from your frontend domain by setting `FRONTEND_URL` in backend environment variables

## Environment Variables Reference

### Frontend (Set in Frontend Vercel Project)
- `VITE_API_BASE_URL`: URL of your deployed backend API

### Backend (Set in Backend Vercel Project)
- `DATABASE_URL`: Database connection string
- `OPENAI_API_KEY`: OpenAI API key
- `NEON_DATABASE_URL`: Neon database connection string
- `BETTER_AUTH_SECRET`: Authentication secret
- `BETTER_AUTH_URL`: URL of your frontend when deployed
- `FRONTEND_URL`: (Optional) URL of your frontend for CORS configuration

## Verification Steps

After deployment:
1. Visit your frontend URL
2. Try to register a new account - this should work without "failed to fetch" errors
3. Try to login - this should work without "failed to fetch" errors
4. Verify that API calls are going to your deployed backend, not localhost