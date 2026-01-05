# GitHub Deployment Setup Guide

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **Vercel CLI**: Install globally with `npm install -g vercel`
3. **GitHub Repository**: Make sure your code is pushed to GitHub

## Setup Steps

### 1. Get Vercel Token

1. Go to [Vercel Dashboard](https://vercel.com/account/tokens)
2. Create a new token with appropriate permissions
3. Copy the token value

### 2. Add Token to GitHub Secrets

1. Go to your GitHub repository
2. Click on "Settings" tab
3. Click on "Secrets and variables" in the left sidebar
4. Click on "Actions"
5. Click "New repository secret"
6. Add the following secrets:
   - Name: `VERCEL_TOKEN`, Value: your vercel token

### 3. Connect GitHub to Vercel (Alternative approach)

Instead of using GitHub Actions, you can directly connect your GitHub repository to Vercel:

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "Add New..." → "Project"
3. Import your GitHub repository
4. Choose the backend directory for backend deployment
5. Choose the frontend directory for frontend deployment
6. Add your environment variables in the Vercel dashboard

### 4. Environment Variables

For backend deployment, add these environment variables in Vercel:

```
DATABASE_URL=your_postgresql_database_url
SECRET_KEY=your_secret_key
GEMINI_API_KEY=your_google_gemini_api_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

For frontend deployment, add these environment variables in Vercel:

```
NEXT_PUBLIC_STREAM_API_KEY=your_stream_chat_api_key
NEXT_PUBLIC_STREAM_USER_TOKEN=your_stream_chat_user_token
NEXT_PUBLIC_API_URL=your_backend_vercel_url
```

## GitHub Actions Deployment

If you prefer to use GitHub Actions for deployment:

1. Push this repository to GitHub
2. Add the `VERCEL_TOKEN` secret to your GitHub repository
3. The workflows will automatically deploy when you push to the `phase3` branch

## Manual Deployment

You can also deploy manually using the Vercel CLI:

### For Backend:
```bash
cd backend
vercel --prod
```

### For Frontend:
```bash
cd frontend
vercel --prod
```

## Troubleshooting

1. **Permission Issues**: Make sure your Vercel token has the correct permissions
2. **Environment Variables**: Ensure all required environment variables are set
3. **Build Errors**: Check the build logs in GitHub Actions or Vercel dashboard
4. **Database Connection**: Verify your DATABASE_URL is accessible from the deployment environment