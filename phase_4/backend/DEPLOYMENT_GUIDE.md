# Backend Deployment Guide

This guide explains how to properly deploy the backend to Vercel to fix authentication and CORS issues.

## Issues Fixed

- Replaced fallback API that returned fake JWT tokens with proper main API
- Enhanced CORS configuration to properly handle cross-origin requests
- Updated dependencies to ensure all required packages are available
- Fixed environment variable validation to support Vercel serverless environment
- Improved authentication token handling for serverless deployments
- Added robust error handling for database connection issues

## Required Environment Variables

Before deploying, ensure the following environment variables are set in the Vercel dashboard:

### Required Variables:
- `DATABASE_URL`: PostgreSQL database connection string (e.g., `postgresql://username:password@host:port/database`)
- `SECRET_KEY`: Strong secret key for JWT token signing (at least 32 characters)
- `BETTER_AUTH_SECRET`: Secret for authentication (at least 32 characters)

### Optional Variables:
- `OPENAI_API_KEY`: Your OpenAI API key (required for AI features)
- `FRONTEND_URL`: Your frontend URL (e.g., `https://your-frontend.vercel.app`)

## Security Requirements

⚠️ **IMPORTANT SECURITY NOTE**: The SECRET_KEY and BETTER_AUTH_SECRET must be at least 32 characters long and should be randomly generated. Using weak or predictable secrets can lead to security vulnerabilities.

Examples of acceptable secrets:
- SECRET_KEY: `my_very_long_secure_secret_key_that_is_at_least_32_chars_long`
- BETTER_AUTH_SECRET: `another_very_secure_randomly_generated_secret_key`

## Deployment Steps

1. **Update Environment Variables Locally**
   - Update your local `.env` file with secure, long secrets (at least 32 characters)
   - This ensures your local environment matches production expectations

2. **Push Changes to Repository**
   ```bash
   git add .
   git commit -m "Fix backend Vercel configuration to use proper main API"
   git push origin main
   ```

3. **Redeploy on Vercel**
   - Go to your Vercel dashboard
   - Select your backend project
   - Trigger a new deployment (it should automatically pick up the changes from the repository)

4. **Set Environment Variables in Vercel Dashboard**
   - Go to your project settings in Vercel
   - Navigate to "Environment Variables"
   - Add the required variables listed above (make sure to use strong, unique values)
   - Ensure you're setting variables for the correct environment (Production/Preview/Development)

5. **Verify Deployment**
   - Check that the deployment succeeds without errors
   - Test the authentication endpoints
   - Verify that CORS issues are resolved

## Expected Behavior After Deployment

- Authentication endpoints (`/auth/login`, `/auth/register`, `/auth/me`) will return real JWT tokens instead of fake ones
- CORS preflight requests will be properly handled
- Dashboard API endpoints (`/dashboard/stats`, `/dashboard/overview`) will be accessible with proper authentication
- All API endpoints will work with proper authentication and authorization
- Environment variable validation will pass successfully in the Vercel environment
- Database connections will work properly with the provided connection string

## Troubleshooting

If you still experience issues after deployment:

1. Check the deployment logs in Vercel for any errors
2. Verify that all required environment variables are correctly set with proper values
3. Ensure that the database connection string is valid and accessible from Vercel
4. Test the backend API endpoints directly using a tool like Postman or curl
5. Check that SECRET_KEY and BETTER_AUTH_SECRET are at least 32 characters long
6. Verify that your database provider allows connections from Vercel's IP ranges
7. Review the `VERCEL_DEPLOYMENT_CHECKLIST.md` for additional troubleshooting steps