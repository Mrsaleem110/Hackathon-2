# Vercel Backend Deployment Checklist

This document provides a step-by-step checklist to successfully deploy the backend to Vercel and resolve common issues.

## Pre-Deployment Checklist

### 1. Environment Variables Setup
Before deploying, ensure the following environment variables are properly configured:

**Required Variables:**
- `DATABASE_URL`: PostgreSQL database connection string (e.g., `postgresql://username:password@host:port/database`)
- `SECRET_KEY`: Strong secret key for JWT token signing (at least 32 characters)
- `BETTER_AUTH_SECRET`: Secret for authentication (at least 32 characters)

**Optional Variables:**
- `OPENAI_API_KEY`: Your OpenAI API key (required for AI features)
- `FRONTEND_URL`: Your frontend URL (e.g., `https://your-frontend.vercel.app`)

### 2. Security Checks
- [ ] SECRET_KEY is at least 32 characters long
- [ ] BETTER_AUTH_SECRET is at least 32 characters long
- [ ] No hardcoded secrets in the codebase
- [ ] Database connection string is properly formatted

### 3. Dependencies Verification
- [ ] `requirements-vercel.txt` contains all necessary packages
- [ ] No conflicting dependencies
- [ ] Python runtime is set to 3.11 in `vercel.json`

## Deployment Steps

### Step 1: Prepare the Repository
```bash
# Navigate to backend directory
cd backend

# Verify environment variables are set
python -c "from src.utils.env_validator import validate_environment; validate_environment()"
```

### Step 2: Link to Vercel Project
```bash
# Install Vercel CLI if not already installed
npm install -g vercel

# Link your project to Vercel
vercel
```

### Step 3: Set Environment Variables in Vercel Dashboard
1. Go to your Vercel dashboard
2. Select your backend project
3. Navigate to Settings → Environment Variables
4. Add the required environment variables listed above

### Step 4: Deploy to Production
```bash
# Deploy to production
vercel --prod
```

## Post-Deployment Verification

### 1. Health Check
Visit `https://your-project-name.vercel.app/health` to verify the API is operational.

### 2. CORS Test
Test CORS headers by making a request from your frontend domain to verify cross-origin requests work properly.

### 3. Authentication Test
Test the authentication endpoints:
- `POST /auth/login`
- `POST /auth/register`
- `GET /auth/me`

### 4. API Endpoints Test
Verify that all major API endpoints are working:
- `/tasks` endpoints
- `/chat` endpoints
- `/dashboard` endpoints
- `/analysis` endpoints

## Troubleshooting Common Issues

### Issue: Environment Variables Not Loading
**Symptoms:**
- Database connection errors
- Authentication failures
- Validation errors

**Solution:**
1. Double-check that all required environment variables are set in the Vercel dashboard
2. Verify variable names match exactly (case-sensitive)
3. Check that variables are set for the correct environment (production vs preview)

### Issue: CORS Errors
**Symptoms:**
- Cross-origin requests failing
- Preflight requests returning errors

**Solution:**
1. Ensure `FRONTEND_URL` is set to your frontend deployment URL
2. Check that the CORS configuration in `main.py` includes your frontend domain
3. Verify that your frontend is making requests to the correct backend URL

### Issue: Database Connection Failures
**Symptoms:**
- Database errors in logs
- API endpoints returning 500 errors
- Authentication not working

**Solution:**
1. Verify the `DATABASE_URL` is correctly formatted
2. Check that your database provider allows connections from Vercel IP ranges
3. Ensure the database credentials are correct
4. Test the database connection string separately

### Issue: Build Failures
**Symptoms:**
- Deployment fails during build step
- Package installation errors
- Python runtime compatibility issues

**Solution:**
1. Verify `requirements-vercel.txt` contains all necessary dependencies
2. Check that the Python runtime in `vercel.json` matches your local version
3. Ensure all dependencies are compatible with Vercel's build environment
4. Look for specific error messages in the build logs

## Configuration Files Overview

### `vercel.json`
Configures the Vercel deployment with:
- Python runtime (3.11)
- Build command using `requirements-vercel.txt`
- Route configuration for FastAPI

### `requirements-vercel.txt`
Production dependencies specifically for Vercel deployment, including:
- FastAPI framework
- Database drivers (PostgreSQL)
- Authentication libraries
- AI integration libraries

### `src/utils/env_validator.py`
Validates environment variables at startup and provides:
- Serverless-compatible fallback values
- Security checks for required variables
- Detailed error messages for troubleshooting

### `src/api/main.py`
Main FastAPI application with:
- Comprehensive CORS configuration
- Error handling with proper response formats
- Dynamic origin detection for Vercel deployments
- Middleware for request processing

## Best Practices for Vercel Deployment

1. **Environment Variables:** Always use Vercel's environment variable system rather than local `.env` files
2. **Secret Keys:** Generate strong, random secret keys for production deployments
3. **Database Connections:** Use connection pooling appropriate for serverless environments
4. **Error Handling:** Implement proper error responses that work well in serverless context
5. **Logging:** Use structured logging for easier debugging in production
6. **Testing:** Thoroughly test all endpoints after deployment

## Rollback Procedure

If deployment issues occur:
1. Identify the problematic changes from the deployment logs
2. Revert the code changes in your repository
3. Trigger a new deployment to revert to a working state
4. Alternatively, use Vercel's deployment history to rollback to a previous version