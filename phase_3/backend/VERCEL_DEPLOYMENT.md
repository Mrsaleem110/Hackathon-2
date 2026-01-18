# Backend Vercel Deployment Configuration

## Environment Variables Setup

When deploying the backend to Vercel, you need to set the following environment variables in your Vercel dashboard:

### Required Variables:
- `DATABASE_URL`: Your PostgreSQL database connection string
- `OPENAI_API_KEY`: Your OpenAI API key
- `NEON_DATABASE_URL`: Your Neon database connection string
- `BETTER_AUTH_SECRET`: Secret for authentication
- `BETTER_AUTH_URL`: URL for Better Auth (set to your frontend URL when deployed)

### Optional Variables for Cross-Origin Requests:
- `FRONTEND_URL`: The URL of your deployed frontend (e.g., `https://your-frontend.vercel.app`)
  - This allows your backend to accept requests from your deployed frontend
  - If not set, the backend will allow all `*.vercel.app` domains when deployed to Vercel

## CORS Configuration

The backend is configured to allow:
- Local development origins (localhost:5173, localhost:5174, localhost:3000)
- Deployed frontend URL (when `FRONTEND_URL` environment variable is set)
- All `*.vercel.app` domains when deployed to Vercel (fallback)

## Deployment Steps

1. Deploy the backend to Vercel first and note the generated URL
2. Set the required environment variables in Vercel dashboard
3. Optionally set `FRONTEND_URL` to your frontend deployment URL
4. Take note of the backend URL for configuring the frontend

## Backend URL Format

After deployment, your backend will be available at:
```
https://your-backend-project-name.vercel.app
```

Use this URL as the `VITE_API_BASE_URL` when deploying the frontend.