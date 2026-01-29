# Quick Vercel Deployment Steps

## Backend Deployment

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Add environment variables to Vercel:
   ```bash
   vercel env add DATABASE_URL --environment production
   vercel env add JWT_SECRET --environment production
   vercel env add OPENAI_API_KEY --environment production
   vercel env add OPENAI_MODEL --environment production
   ```

3. Deploy backend:
   ```bash
   vercel --prod
   ```

4. Note the backend URL (e.g., `https://hackathon-2-p-3-backend.vercel.app`)

## Frontend Deployment

1. Navigate to frontend directory:
   ```bash
   cd ../frontend
   ```

2. Add environment variables to Vercel:
   ```bash
   vercel env add VITE_API_BASE_URL --environment production
   # Use the backend URL from step 3 above
   vercel env add NEXT_PUBLIC_OPENAI_API_KEY --environment production
   ```

3. Deploy frontend:
   ```bash
   vercel --prod
   ```

## Important URLs from Your Current Setup

Based on your existing configuration, your deployments should be accessible at:
- Backend: `https://hackathon-2-p-3-backend.vercel.app`
- Frontend: `https://hackathon-2-p-3-frontend.vercel.app`

These are already configured in your `frontend/vercel.json` file for API rewrites.