---
id: 3
title: Update Env Vars for Vercel Deployment
stage: refactor
date_iso: 2026-01-23
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: unknown
command: manual
labels: ["vercel", "environment", "configuration", "cors", "deployment"]
links_spec: null
links_ticket: null
links_adr: null
links_pr: null
files_yaml: |
  - frontend/.env
tests_yaml: |
  - none
---

# Update Env Vars for Vercel Deployment

## Prompt Text
```
login:1 Access to fetch at 'https://hackathon-2-p-3.vercel.app//auth/login' from origin 'https://hackathon-2-sooty.vercel.app' has been blocked by CORS policy: Response to preflight request doesn't pass access control check: Redirect is not allowed for a preflight request.
```

## Response Text
Updated frontend environment variables to use correct deployed backend URL to fix CORS issues between frontend and backend on Vercel deployment.

## Context
User experienced CORS errors when trying to authenticate on Vercel deployment. The frontend (on hackathon-2-sooty.vercel.app) was trying to access the backend (on hackathon-2-p-3.vercel.app) but was getting blocked by CORS policy due to redirect issues during preflight requests.

## Outcome Impact
- Updated VITE_API_BASE_URL in frontend to point to deployed backend
- Fixed potential URL construction issues for API requests
- Should resolve CORS preflight redirect errors when backend is redeployed with proper CORS configuration

## Technical Details
- Updated frontend/.env to use deployed backend URL instead of localhost
- VITE_API_BASE_URL changed from http://localhost:8001 to https://hackathon-2-p-3.vercel.app
- VITE_BETTER_AUTH_URL also updated to use the same backend domain
- Need to redeploy backend with proper CORS configuration for frontend domain

## Tests Summary
none

## Files Summary
- frontend/.env - Updated API URLs for Vercel deployment

## Next Prompts
- Deploy updated frontend with new environment variables
- Ensure backend has proper CORS configuration for frontend domain

## Reflection Note
When deploying to different domains, ensure both frontend and backend have proper CORS configuration and environment variables updated for production.

## Failure Modes Observed
CORS preflight redirect errors can occur when backend doesn't properly handle OPTIONS requests or when there are redirect loops during preflight.

## Next Experiment to Improve Prompt Quality
N/A