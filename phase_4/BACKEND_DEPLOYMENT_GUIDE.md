# Backend Deployment Guide

This guide explains how to deploy the AI-Powered Todo Chatbot backend to Vercel.

## Prerequisites

1. A Vercel account (sign up at https://vercel.com)
2. Your NeonDB database connection string
3. Secret keys for JWT authentication
4. OpenAI API key (optional, for AI features)

## Deployment Steps

### 1. Environment Variables Setup

Set the following environment variables in your Vercel project:

#### Required Variables:
- `DATABASE_URL`: Your NeonDB connection string
- `NEON_DATABASE_URL`: Your NeonDB connection string (same as above)
- `SECRET_KEY`: At least 32-character secret for JWT tokens
- `BETTER_AUTH_SECRET`: At least 32-character secret for authentication

#### Optional Variables:
- `OPENAI_API_KEY`: Your OpenAI API key for AI features
- `FRONTEND_URL`: Your frontend deployment URL for CORS
- `CORS_ORIGINS`: Comma-separated list of allowed origins
- `BETTER_AUTH_URL`: Your backend deployment URL

### 2. Vercel Project Configuration

The project is already configured for Vercel deployment with:
- Python 3.11 runtime
- Serverless function setup using modern functions property
- Proper CORS handling for Vercel deployments
- Fallback mechanisms for serverless environments
- Dependencies automatically handled via requirements.txt

### 3. Deploy to Vercel

#### Option 1: Using Vercel CLI
```bash
npm install -g vercel
vercel --prod
```

#### Option 2: Connect GitHub Repository
1. Push this code to your GitHub repository
2. Go to https://vercel.com/dashboard
3. Click "Add New" → "Project"
4. Find and import your repository
5. Vercel will automatically detect the Python project
6. Add your environment variables in the project settings
7. Click "Deploy"

### 4. Post-Deployment Steps

1. Verify the deployment by visiting your Vercel URL
2. Test the health check endpoint: `https://your-project.vercel.app/health`
3. Test the debug endpoint: `https://your-project.vercel.app/debug/test`
4. Update your frontend to use the new backend URL

## Important Endpoints

- `/`: Root endpoint showing API status
- `/health`: Health check endpoint
- `/debug/test`: Simple test endpoint
- `/debug/cors`: CORS configuration debug endpoint
- `/debug/routes`: List all available routes
- `/auth/*`: Authentication endpoints
- `/tasks/*`: Task management endpoints
- `/chat/*`: Chat functionality endpoints
- `/dashboard/*`: Dashboard endpoints
- `/analysis/*`: Analytics endpoints

## Troubleshooting

### Common Issues:
1. **CORS errors**: Ensure FRONTEND_URL is set correctly in environment variables
2. **Database connection errors**: Verify DATABASE_URL is set correctly
3. **Authentication failures**: Check SECRET_KEY and BETTER_AUTH_SECRET are properly set

### Debugging:
- Use `/debug/cors` to check CORS configuration
- Use `/debug/routes` to see all available endpoints
- Check Vercel logs in the dashboard for runtime errors

## Security Notes

- Never commit secret keys to version control
- Use strong, randomly generated secrets for SECRET_KEY and BETTER_AUTH_SECRET
- Enable production mode (DEBUG=false) for live deployments
- Regularly rotate your API keys and database credentials

## Scaling Recommendations

- Monitor database connections in NeonDB dashboard
- Consider using connection pooling for high-traffic applications
- Implement caching for frequently accessed data
- Set up proper monitoring and alerting