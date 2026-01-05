# Deployment Guide for Phase 3 Todo AI Chat Application

## Backend Deployment (Vercel)

### Prerequisites
- Vercel account
- GitHub account connected to Vercel
- Your project pushed to a GitHub repository

### Steps

1. **Prepare Environment Variables**
   - Create a `.env` file with the following variables:
   ```
   DATABASE_URL=your_postgresql_database_url
   SECRET_KEY=your_secret_key
   GEMINI_API_KEY=your_google_gemini_api_key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

2. **Vercel Configuration**
   - The `vercel.json` file is already configured in the backend directory
   - The `api.py` file is properly set up for Vercel deployment with the Mangum adapter

3. **Deploy to Vercel**
   - Go to https://vercel.com
   - Import your GitHub repository
   - In the project settings, make sure:
     - Framework Preset: None/Other
     - Root Directory: `backend`
     - Build Command: `pip install -r requirements.txt`
     - Output Directory: (leave empty)
   - Add the environment variables in the Vercel dashboard under Settings > Environment Variables

## Frontend Deployment (Vercel)

### Steps

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Create `.env.local` file** with:
   ```
   NEXT_PUBLIC_STREAM_API_KEY=your_stream_chat_api_key
   NEXT_PUBLIC_STREAM_USER_TOKEN=your_stream_chat_user_token
   NEXT_PUBLIC_API_URL=your_backend_vercel_url
   ```

3. **Deploy to Vercel**
   - Go to https://vercel.com
   - Import your GitHub repository
   - In the project settings:
     - Framework Preset: Next.js
     - Root Directory: `frontend`
   - Add the environment variables in the Vercel dashboard

## Alternative: Manual Deployment

### For Backend:
1. Ensure your `api.py` file is properly configured (it should be already)
2. Make sure all dependencies are in `requirements.txt` (already done)
3. Set up your environment variables
4. Deploy to your preferred platform (Heroku, Railway, etc.)

### For Frontend:
1. Make sure to update the API URL in the frontend to point to your deployed backend
2. Configure Stream Chat with your API keys
3. Deploy to Netlify, Vercel, or your preferred platform

## Troubleshooting Common Issues

### 1. Module Import Errors
- Ensure all imports in `api.py` are correct and all dependencies are in `requirements.txt`
- Check that all model files are properly imported

### 2. Database Connection Issues
- Verify your `DATABASE_URL` is correctly set
- Make sure your database is accessible from the deployment environment

### 3. CORS Issues
- The CORS middleware is already configured to work with Vercel deployments
- If you have custom domain requirements, update the allowed origins in `api.py`

### 4. API Keys Not Working
- Double-check that your GEMINI_API_KEY and other keys are properly set in environment variables
- Verify that your Stream Chat API keys are correctly configured in the frontend

## Important Notes

- The `api.py` file has been configured specifically for serverless deployment
- Database initialization happens on application startup
- The application uses Google Gemini for AI responses
- Stream Chat is configured for real-time messaging
- User authentication is handled with JWT tokens