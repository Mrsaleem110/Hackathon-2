# Backend Vercel Deployment Configuration

## Environment Variables Setup

When deploying the backend to Vercel, you need to set the following environment variables in your Vercel dashboard:

### Required Variables:
- `DATABASE_URL`: Your PostgreSQL database connection string
- `SECRET_KEY`: Strong secret key for JWT token signing (at least 32 characters)
- `BETTER_AUTH_SECRET`: Secret for authentication (at least 32 characters)
- `OPENAI_API_KEY`: Your OpenAI API key (required for AI features)

### Optional Variables for Cross-Origin Requests:
- `FRONTEND_URL`: The URL of your deployed frontend (e.g., `https://your-frontend.vercel.app`)
  - This allows your backend to accept requests from your deployed frontend
  - If not set, the backend will allow all `*.vercel.app` domains when deployed to Vercel

## Security Requirements

⚠️ **CRITICAL SECURITY NOTICE**: Both `SECRET_KEY` and `BETTER_AUTH_SECRET` must be at least 32 characters long and should consist of random, unpredictable characters. Weak secrets can compromise your entire authentication system.

Example of a secure secret generation:
```bash
# Generate a secure random secret (at least 32 characters)
openssl rand -hex 32
```

## CORS Configuration

The backend is configured to allow:
- Local development origins (localhost:5173, localhost:5174, localhost:3000, etc.)
- Deployed frontend URL (when `FRONTEND_URL` environment variable is set)
- All `*.vercel.app` domains when deployed to Vercel (fallback)
- Dynamic origin detection for Vercel preview deployments

## Deployment Steps

1. Deploy the backend to Vercel first and note the generated URL
2. Set the required environment variables in Vercel dashboard (ensure secrets are at least 32 characters)
3. Optionally set `FRONTEND_URL` to your frontend deployment URL
4. Take note of the backend URL for configuring the frontend

## Backend URL Format

After deployment, your backend will be available at:
```
https://your-backend-project-name.vercel.app
```

Use this URL as the `VITE_API_BASE_URL` when deploying the frontend.

## Troubleshooting Common Issues

### Environment Variable Validation Failures
- Ensure SECRET_KEY is at least 32 characters
- Verify BETTER_AUTH_SECRET meets the length requirement
- Check that all required variables are set in the correct environment (Production/Preview)

### Database Connection Issues
- Verify your database provider allows connections from Vercel's IP ranges
- Ensure the DATABASE_URL format is correct for your database provider
- Test the connection string independently before deployment

### CORS Issues
- Confirm FRONTEND_URL is set to your exact frontend domain
- Check that the frontend is making requests to the correct backend endpoint
- Review browser console for specific CORS error messages