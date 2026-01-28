# Vercel Environment Variables Setup Guide

This document outlines the environment variables required for deploying both the frontend and backend of the AI-Powered Todo Chatbot on Vercel.

## Backend Environment Variables for Vercel Deployment

### Required Environment Variables:

1. **`NEON_DATABASE_URL`** (Required)
   - Your Neon PostgreSQL database connection string
   - Format: `postgresql://username:password@host/database?sslmode=require`
   - This is the primary database connection for your application

2. **`OPENAI_API_KEY`** (Required if using OpenAI features)
   - Your OpenAI API key for AI-powered features
   - Format: `sk-...` (starts with sk-)

3. **`BETTER_AUTH_SECRET`** (Required for authentication)
   - Secret key used for JWT token signing/verification
   - Should be a strong, random string
   - Used for both custom JWT and Better Auth token validation

4. **`OPENAI_MODEL`** (Optional, defaults to gpt-3.5-turbo)
   - The OpenAI model to use for AI features
   - Default: `gpt-3.5-turbo`

### Optional Environment Variables:

5. **`FRONTEND_URL`** (Optional)
   - Your deployed frontend URL
   - Default: `https://hackathon-2-p-3-frontend.vercel.app`
   - Used for CORS configuration

6. **`DATABASE_URL`** (Optional fallback)
   - Fallback database URL if NEON_DATABASE_URL is not set
   - Will default to SQLite if neither is set (not recommended for production)

7. **`BETTER_AUTH_URL`** (Optional)
   - Better Auth server URL
   - Default: `http://localhost:3000` (but you should update for production)

8. **`MCP_SERVER_URL`** (Optional)
   - MCP server URL if you're using MCP features
   - Default: `http://localhost:3000`

9. **`DEBUG`** (Optional)
   - Set to `"true"` to enable detailed error messages
   - Default: disabled for security reasons

## Frontend Environment Variables for Vercel Deployment

### Required Environment Variables:

1. **`VITE_API_BASE_URL`** (Required)
   - The URL of your deployed backend API
   - For production: should be your deployed backend URL (e.g., `https://hackathon-2-p-3-backend.vercel.app`)
   - This tells the frontend where to send API requests
   - In development: typically `http://localhost:8001`

### Optional Environment Variables:

2. **`NEXT_PUBLIC_OPENAI_API_KEY`** (Optional - NOT RECOMMENDED FOR PRODUCTION)
   - Your OpenAI API key for frontend OpenAI features
   - Format: `sk-...` (starts with sk-)
   - ⚠️ **WARNING**: Including API keys in frontend code is a security risk as they will be exposed to clients

3. **`NEXT_PUBLIC_OPENAI_DOMAIN_KEY`** (Optional - NOT RECOMMENDED FOR PRODUCTION)
   - Domain key for OpenAI ChatKit
   - Format: `domain_pk_...` (starts with domain_pk_)

## Security Recommendations:

⚠️ **IMPORTANT SECURITY NOTES:**
- Never expose your actual API keys in public repositories
- Use strong, randomly generated secrets for `BETTER_AUTH_SECRET`
- **DO NOT** put `NEXT_PUBLIC_*` API keys in production as they will be exposed to users in the browser
- Rotate your API keys periodically
- Consider using different keys for development and production
- Remove any hardcoded credentials from your code before deployment
- API keys should be kept server-side. The frontend should communicate with your backend, which then makes requests to OpenAI using the API key stored securely on the backend

## How to Set Up in Vercel Dashboard:

### For Backend:
1. Go to your Vercel dashboard
2. Select your backend project
3. Go to Settings → Environment Variables
4. Add each variable with its corresponding value

### For Frontend:
1. Go to your Vercel dashboard
2. Select your frontend project
3. Go to Settings → Environment Variables
4. Add each variable with its corresponding value

## Additional Configuration:

### Backend:
- Runtime: Python 3.11 (as specified in `vercel.json`)
- Build command: Vercel will automatically detect from `requirements.txt`
- Install command: Vercel will automatically install dependencies from `requirements.txt`

### Frontend:
- Framework: Vite (will be detected automatically from `package.json`)
- Build command: `npm run build` (detected automatically)
- Output directory: `dist` (configured in `vite.config.js`)
- Install command: `npm install` (detected automatically)

## Vercel Rewrites (Frontend):

The `frontend/vercel.json` file is already configured with rewrites that will route API requests from the frontend to your backend:
- `/api/auth/*` → backend auth endpoints
- `/auth/*` → backend auth endpoints
- `/tasks/*` → backend tasks endpoints
- `/chat/*` → backend chat endpoints
- `/dashboard/*` → backend dashboard endpoints
- `/analysis/*` → backend analysis endpoints

This means API requests from the frontend will be automatically forwarded to your backend via Vercel's rewrite mechanism, so the frontend can use relative paths in production while still communicating with your backend service.