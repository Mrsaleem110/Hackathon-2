# Vercel Crash Troubleshooting Guide

## Common Vercel Backend Crashes and Fixes

### 1. Import Errors
**Symptoms:** ModuleNotFoundError, ImportError during startup
**Causes:** Missing dependencies, incorrect import paths, circular imports
**Solution:** Use the crash-resistant app_crash_fix.py which handles import failures gracefully

### 2. Environment Variables Missing
**Symptoms:** Runtime errors related to missing configuration
**Causes:** Not setting required environment variables in Vercel dashboard
**Solution:** Ensure these are set in Vercel environment variables:
- `SECRET_KEY` (at least 32 chars)
- `DATABASE_URL` (Neon DB connection string)
- `BETTER_AUTH_SECRET` (at least 32 chars)

### 3. Database Connection Issues
**Symptoms:** Database errors, timeouts, connection failures
**Causes:** Incorrect DB URL, firewall restrictions, SSL issues
**Solution:** Verify Neon DB connection string format with proper SSL parameters

### 4. Memory Issues
**Symptoms:** Out of memory errors, function timeouts
**Causes:** Large dependencies, memory leaks, inefficient code
**Solution:** Use optimized dependencies and efficient code patterns

## Recovery Steps

### Step 1: Immediate Fix
1. Ensure `app_crash_fix.py` is used as the entry point (updated in vercel.json)
2. Verify environment variables are set in Vercel dashboard
3. Redeploy the application

### Step 2: Verify Environment Variables in Vercel Dashboard
Go to your Vercel project settings → Environment Variables and ensure these are set:
```
SECRET_KEY=your-very-long-secret-key-at-least-32-chars-change-in-production
DATABASE_URL=your-neon-database-connection-string
BETTER_AUTH_SECRET=your-very-long-better-auth-secret-at-least-32-chars-change-in-production
```

### Step 3: Test the Fix
1. Deploy with: `vercel --prod`
2. Visit: `https://your-app.vercel.app/health`
3. Should return: `{"status": "healthy", "platform": "vercel", "deployment": "success"}`

### Step 4: Gradual Restoration
Once stable, you can gradually move back to the full-featured app.py by:
1. Testing individual components
2. Adding back routes one by one
3. Monitoring for stability

## Quick Verification Commands

```bash
# Test local environment validation
python -c "from src.utils.env_validator import validate_environment; validate_environment()"

# Check if app loads without crashing
python -c "import app_crash_fix; print('App loaded successfully')"
```

## Emergency Rollback
If issues persist:
1. Revert to the original app.py
2. Ensure all environment variables are properly set in Vercel
3. Check Vercel build logs for specific error messages
4. Address the root cause based on error logs

## Prevention Measures
- Always test environment variables locally before deployment
- Use fallback values for critical configuration
- Implement graceful degradation for missing services
- Monitor deployment logs closely during initial deployment

## Support Endpoints
After fixing the crash, these endpoints should be available:
- `GET /` - Main health status
- `GET /health` - Health check
- `GET /crash_health` - Crash-specific health check
- `GET /debug/info` - Debug information (fallback mode)