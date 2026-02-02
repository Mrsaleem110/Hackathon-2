# Backend Deployment Guide

This guide explains how to properly deploy the backend to Vercel to fix authentication and CORS issues.

## Issues Fixed

- Replaced fallback API that returned fake JWT tokens with proper main API
- Enhanced CORS configuration to properly handle cross-origin requests
- Updated dependencies to ensure all required packages are available

## Required Environment Variables

Before deploying, ensure the following environment variables are set in the Vercel dashboard:

### Required Variables:
- `DATABASE_URL`: PostgreSQL database connection string (e.g., `postgresql://username:password@host:port/database`)
- `SECRET_KEY`: Strong secret key for JWT token signing (at least 32 characters)
- `BETTER_AUTH_SECRET`: Secret for authentication (at least 32 characters)

### Optional Variables:
- `OPENAI_API_KEY`: Your OpenAI API key (required for AI features)
- `FRONTEND_URL`: Your frontend URL (e.g., `https://your-frontend.vercel.app`)

## Deployment Steps

1. **Push Changes to Repository**
   ```bash
   git add .
   git commit -m "Fix backend Vercel configuration to use proper main API"
   git push origin main
   ```

2. **Redeploy on Vercel**
   - Go to your Vercel dashboard
   - Select your backend project
   - Trigger a new deployment (it should automatically pick up the changes from the repository)

3. **Set Environment Variables in Vercel Dashboard**
   - Go to your project settings in Vercel
   - Navigate to "Environment Variables"
   - Add the required variables listed above

4. **Verify Deployment**
   - Check that the deployment succeeds without errors
   - Test the authentication endpoints
   - Verify that CORS issues are resolved

## Expected Behavior After Deployment

- Authentication endpoints (`/auth/login`, `/auth/register`, `/auth/me`) will return real JWT tokens instead of fake ones
- CORS preflight requests will be properly handled
- Dashboard API endpoints (`/dashboard/stats`, `/dashboard/overview`) will be accessible with proper authentication
- All API endpoints will work with proper authentication and authorization

## Troubleshooting

If you still experience issues after deployment:

1. Check the deployment logs in Vercel for any errors
2. Verify that all required environment variables are correctly set
3. Ensure that the database connection string is valid
4. Test the backend API endpoints directly using a tool like Postman or curl