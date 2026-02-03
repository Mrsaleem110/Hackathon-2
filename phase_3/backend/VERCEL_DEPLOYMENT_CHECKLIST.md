# Vercel Deployment Checklist for FastAPI + Neon + Better Auth

## Pre-Deployment Checklist

### 1. Environment Variables Setup
- [ ] `NEON_DATABASE_URL`: PostgreSQL connection string from Neon
- [ ] `SECRET_KEY`: At least 32 characters long (for JWT)
- [ ] `BETTER_AUTH_SECRET`: At least 32 characters long (for Better Auth)
- [ ] `BETTER_AUTH_URL`: Your Vercel backend URL
- [ ] `FRONTEND_URL`: Your frontend URL
- [ ] `OPENAI_API_KEY`: (optional) for AI features

### 2. Security Checks
- [ ] All secrets are at least 32 characters long
- [ ] No hardcoded secrets in the codebase
- [ ] Database URL is properly formatted
- [ ] SSL is enabled for database connections

### 3. Dependencies Verification
- [ ] `requirements-vercel.txt` contains all necessary packages
- [ ] Python runtime set to 3.11 in `vercel.json`
- [ ] All dependencies compatible with Vercel

### 4. Better Auth Integration
- [ ] Better Auth server is configured separately (if using)
- [ ] JWT validation works with Better Auth tokens
- [ ] Callback endpoints are properly configured

## Deployment Steps

### Step 1: Verify Local Setup
```bash
# Navigate to backend directory
cd backend

# Test environment validation
python -c "from src.utils.env_validator import validate_environment; validate_environment()"
```

### Step 2: Install Vercel CLI
```bash
npm install -g vercel
```

### Step 3: Set Environment Variables in Vercel Dashboard
1. Go to your Vercel dashboard
2. Select your backend project
3. Navigate to Settings → Environment Variables
4. Add all required environment variables listed above

### Step 4: Deploy
```bash
# Deploy to preview
vercel

# Deploy to production
vercel --prod
```

## Post-Deployment Verification

### 1. Health Check
Visit `https://your-project-name.vercel.app/health` to verify the API is operational.

### 2. Authentication Test
Test authentication endpoints:
- `POST /auth/login`
- `POST /auth/register`
- `GET /auth/me`

### 3. Database Connection
- Verify that database operations work properly
- Test creating and retrieving data

### 4. Better Auth Integration
- Test JWT token validation
- Verify compatibility with Better Auth tokens

### 5. CORS Configuration
- Test cross-origin requests from your frontend
- Verify preflight requests work properly

## Common Issues and Solutions

### Issue: Environment Variables Not Loading
**Symptoms:**
- Database connection errors
- Authentication failures

**Solution:**
1. Verify all required environment variables are set in Vercel dashboard
2. Check variable names match exactly (case-sensitive)
3. Ensure variables are set for the correct environment (production vs preview)

### Issue: Database Connection Failures
**Symptoms:**
- 500 errors on database-dependent endpoints
- Connection timeouts

**Solution:**
1. Verify `NEON_DATABASE_URL` is correctly formatted
2. Check Neon database settings allow external connections
3. Ensure the database credentials are correct

### Issue: Authentication Problems
**Symptoms:**
- Login/register not working
- JWT validation failing

**Solution:**
1. Ensure `SECRET_KEY` and `BETTER_AUTH_SECRET` are properly set
2. Verify they are at least 32 characters long
3. Check JWT token format and validation logic

### Issue: CORS Errors
**Symptoms:**
- Cross-origin requests failing
- Preflight requests blocked

**Solution:**
1. Ensure `FRONTEND_URL` is set correctly
2. Verify CORS configuration in `main.py`
3. Check that frontend is making requests to correct backend URL

## Rollback Plan

If deployment issues occur:
1. Identify the problematic changes from deployment logs
2. Revert code changes in repository
3. Trigger new deployment to revert to working state
4. Or use Vercel's deployment history to rollback

## Monitoring and Maintenance

### Logging
- Monitor Vercel logs for errors
- Check for authentication failures
- Track database connection issues

### Performance
- Monitor response times
- Check for database query performance
- Verify authentication token validation speed

### Security
- Regularly rotate secrets
- Monitor for suspicious authentication attempts
- Keep dependencies updated