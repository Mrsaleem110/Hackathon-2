# Complete Vercel Deployment Guide for Frontend & Backend

This guide will walk you through deploying both your React/Vite frontend and FastAPI backend to Vercel.

## Project Architecture

Your project follows a microservices architecture with:
- **Frontend**: React/Vite application in `/frontend/` directory
- **Backend**: FastAPI application in `/backend/` directory
- **Authentication**: Hybrid system with Better Auth and custom JWT
- **Database**: PostgreSQL via NeonDB

Because these are separate applications in different directories with different tech stacks, they need to be deployed as separate Vercel projects.

## Prerequisites

1. Install the Vercel CLI globally:
   ```bash
   npm install -g vercel
   ```

2. Create accounts on:
   - [Vercel](https://vercel.com/) for hosting
   - [NeonDB](https://neon.tech/) (already configured in your project)

3. **Important**: You will deploy your frontend and backend as separate Vercel projects since they are in different directories with different technologies (React/Vite frontend and FastAPI backend).

## Part 1: Deploy Backend to Vercel

### Step 1: Navigate to the backend directory
```bash
cd backend
```

### Step 2: Set up environment variables
Before deploying, you need to add your environment variables to Vercel. You can do this in two ways:

**Option A: Using Vercel CLI (recommended)**
```bash
vercel env add --environment production
```
Then add each variable:
- `DATABASE_URL`: Your PostgreSQL connection string from NeonDB
- `JWT_SECRET`: Your secret key for JWT signing
- `OPENAI_API_KEY`: Your OpenAI API key
- `OPENAI_MODEL`: Your preferred OpenAI model (e.g., gpt-3.5-turbo)

**Option B: Through Vercel Dashboard**
1. Go to your Vercel dashboard
2. Select your project
3. Go to Settings → Environment Variables
4. Add the same variables as above

### Step 3: Deploy the backend
```bash
vercel --prod
```

Note down the backend URL (it will look like `https://your-project-git-main-username.vercel.app` or `https://your-project.vercel.app`).

### Step 4: Update frontend environment variables
After deploying the backend, you'll need to update the frontend's API base URL to point to your deployed backend.

## Part 2: Deploy Frontend to Vercel

### Step 1: Navigate to the frontend directory
```bash
cd ../frontend
```

### Step 2: Update environment variables
In your frontend `.env` file, change the `VITE_API_BASE_URL` to your deployed backend URL:

```env
VITE_API_BASE_URL=https://your-deployed-backend-url.vercel.app
NEXT_PUBLIC_OPENAI_API_KEY=your_openai_api_key
```

### Step 3: Set up environment variables in Vercel
```bash
vercel env add --environment production
```
Add:
- `VITE_API_BASE_URL`: Your deployed backend URL
- `NEXT_PUBLIC_OPENAI_API_KEY`: Your OpenAI API key (or remove if not needed on frontend)

### Step 4: Deploy the frontend
```bash
vercel --prod
```

## Part 3: Configure Production URLs in Backend

After deploying both, you need to update the CORS configuration in your backend to include your frontend's production URL.

### Step 1: Update CORS origins in backend
In `backend/src/api/main.py`, update the `cors_origins` list to include your frontend's Vercel URL:

```python
cors_origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5173",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:8001",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8001",
    "https://your-frontend-project.vercel.app",  # Add your frontend URL here
    "https://your-backend-project.vercel.app",   # Add your backend URL here
    frontend_url,
]
```

### Step 2: Redeploy backend with updated CORS
```bash
cd ../backend
vercel --prod
```

## Part 4: Configure API Rewrites (Optional but Recommended)

Your frontend already has a `vercel.json` that rewrites API calls to the backend. Make sure it points to your deployed backend:

In `frontend/vercel.json`:
```json
{
  "rewrites": [
    { "source": "/api/auth/:path*", "destination": "https://your-deployed-backend.vercel.app/auth/:path*" },
    { "source": "/auth/:path*", "destination": "https://your-deployed-backend.vercel.app/auth/:path*" },
    { "source": "/api/:path*", "destination": "https://your-deployed-backend.vercel.app/api/:path*" },
    { "source": "/tasks/:path*", "destination": "https://your-deployed-backend.vercel.app/tasks/:path*" },
    { "source": "/chat/:path*", "destination": "https://your-deployed-backend.vercel.app/chat/:path*" },
    { "source": "/dashboard/:path*", "destination": "https://your-deployed-backend.vercel.app/dashboard/:path*" },
    { "source": "/analysis/:path*", "destination": "https://your-deployed-backend.vercel.app/analysis/:path*" },
    { "source": "/(.*)", "destination": "/" }
  ]
}
```

## Part 5: Testing Your Deployment

1. Visit your frontend URL to test the application
2. Check that API calls are working by opening browser developer tools and looking for network errors
3. Test authentication and other core functionality

## Troubleshooting

### Common Issues:

1. **CORS errors**: Make sure both your frontend and backend URLs are in the CORS configuration
2. **Database connection errors**: Verify your `DATABASE_URL` environment variable is correct
3. **Authentication issues**: Check that JWT secrets match between frontend and backend
4. **API calls failing**: Ensure your frontend's `VITE_API_BASE_URL` points to the correct backend URL

### Debugging Endpoints:

Your backend has several useful debugging endpoints:
- `GET /debug/routes` - Lists all registered API routes
- `GET /debug/cors` - Shows CORS configuration
- `GET /debug/test` - Simple test endpoint
- `GET /health` - Health check endpoint

## Environment Variables Reference

### Backend Environment Variables:
- `DATABASE_URL` - PostgreSQL database connection string
- `JWT_SECRET` - Secret key for JWT token signing
- `OPENAI_API_KEY` - OpenAI API key
- `OPENAI_MODEL` - Default OpenAI model to use

### Frontend Environment Variables:
- `VITE_API_BASE_URL` - Base URL for API calls to backend
- `NEXT_PUBLIC_OPENAI_API_KEY` - OpenAI API key (if needed on frontend)

## Security Considerations

1. **Never expose sensitive keys in frontend code**
2. **Use strong, unique JWT secrets**
3. **Always use HTTPS in production**
4. **Regularly rotate your API keys**
5. **Monitor your database connection limits**

## Updating Deployments

To update your deployments after making changes:

1. For frontend: Navigate to `frontend/` directory and run `vercel --prod`
2. For backend: Navigate to `backend/` directory and run `vercel --prod`

You can also connect your GitHub repository to Vercel for automatic deployments on push.

## Monitoring and Logs

1. Check your Vercel dashboard for deployment status
2. Use `vercel logs` command to view deployment logs
3. Monitor your NeonDB dashboard for database connection metrics