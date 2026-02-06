# Clean Vercel Deployment Guide

This guide addresses the common Vercel deployment error: `404: NOT_FOUND Code: DEPLOYMENT_NOT_FOUND ID: dxb1::84s5g-1770194143676-c0e97d033b1a`

## Problem Analysis

The error occurs when:
- Vercel tries to access a previous deployment that no longer exists
- Local Vercel configuration is out of sync with the remote project
- There are conflicting deployment states

## Solution Steps

### Method 1: Use the Clean Deployment Script

1. **Run the clean deployment script:**
```bash
python clean_deploy.py
```

This script will:
- Remove existing Vercel configuration
- Verify your files are correct
- Perform a fresh deployment

### Method 2: Manual Clean Deployment

1. **Navigate to the backend directory:**
```bash
cd backend
```

2. **Remove existing Vercel configuration:**
```bash
rm -rf .vercel .env.local
```

3. **Deploy fresh:**
```bash
vercel --prod --force
```

### Method 3: Windows Batch File (Windows users)

1. **Run the batch file:**
```cmd
deploy_clean.bat
```

## Pre-Deployment Checklist

Before deploying, ensure:

✅ `backend/app.py` exists and is the main application file
✅ `backend/requirements.txt` exists with all dependencies
✅ `backend/vercel.json` has only `functions` property (no `builds`)
✅ You're logged into Vercel CLI (`vercel login`)
✅ Environment variables will be set in Vercel dashboard (not locally)

## Setting Environment Variables

After successful deployment:

1. Go to your [Vercel dashboard](https://vercel.com/dashboard)
2. Select your project
3. Go to Settings → Environment Variables
4. Add these required variables:
   - `DATABASE_URL` - Your NeonDB connection string
   - `SECRET_KEY` - JWT secret (at least 32 characters)
   - `BETTER_AUTH_SECRET` - Auth secret (at least 32 characters)
   - `OPENAI_API_KEY` - OpenAI API key (optional)

## Expected Result

After clean deployment, you should see:
- A successful deployment message
- A new deployment URL ending in `.vercel.app`
- All API endpoints accessible
- Health check at `https://your-app.vercel.app/health`

## Troubleshooting

If you still face issues:

1. **Check Vercel login:**
```bash
vercel whoami
```

2. **Verify the vercel.json:**
```bash
cat vercel.json
```
Should only contain `functions`, not `builds`.

3. **Test locally first:**
```bash
python -c "from src.api.main import app; print('Import successful')"
```

## Success Confirmation

Once deployed, test these endpoints:
- `https://your-app.vercel.app/` - Should return API info
- `https://your-app.vercel.app/health` - Should return health status
- `https://your-app.vercel.app/debug/test` - Should return test success