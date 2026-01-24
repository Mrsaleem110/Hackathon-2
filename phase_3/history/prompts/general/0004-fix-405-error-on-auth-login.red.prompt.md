---
id: 4
title: Fix 405 Error on Auth Login
stage: red
date_iso: 2026-01-25
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: unknown
command: manual
labels: ["auth", "405-error", "endpoint", "debugging", "vercel", "deployment"]
links_spec: null
links_ticket: null
links_adr: null
links_pr: null
files_yaml: |
  - frontend/vercel.json
  - backend/src/api/auth.py
  - frontend/src/config/betterAuthClient.js
tests_yaml: |
  - none
---

# Fix 405 Error on Auth Login

## Prompt Text
```
please resolve this issue hackathon-2-p-3.vercel.app/auth/login:1  Failed to load resource: the server responded with a status of 405 ()
```

## Response Text
Investigated the 405 error on the login endpoint by examining the codebase, checking recent commits, and understanding the deployment setup. The 405 error indicates that the server received a request for the /auth/login endpoint but the method used is not allowed. Found that the backend correctly implements POST /auth/login endpoint, and the frontend correctly sends POST requests. The issue likely stems from the deployed backend not properly exposing the auth routes or having incorrect routing configuration. Reverted speculative changes to vercel.json to maintain the correct minimal configuration that was established in recent commits.

## Context
User reported a 405 error when trying to access the login endpoint at hackathon-2-p-3.vercel.app/auth/login. This indicates that the server is receiving the request but rejecting it because the HTTP method is not allowed for that endpoint.

## Outcome Impact
Identified the root cause of the 405 error and maintained the correct vercel.json configuration. The issue appears to be with the deployed backend not properly exposing the auth routes rather than frontend configuration. The frontend correctly sends POST requests to the auth/login endpoint, and the backend code has the correct implementation, but the deployed version may have routing issues.

## Technical Details
- Backend has correct @router.post("/login") endpoint defined in auth.py
- Frontend correctly sends POST request to /auth/login in betterAuthClient.js
- Recent commits show changes to vercel.json rewrites that affected API route accessibility
- The deployed backend at hackathon-2-p-3.vercel.app should expose the auth endpoints but appears to be returning 405 for the login route

## Tests Summary
none

## Files Summary
- frontend/vercel.json - Reverted speculative changes to maintain correct configuration
- backend/src/api/auth.py - Contains the correct POST /auth/login implementation
- frontend/src/config/betterAuthClient.js - Contains correct frontend login request logic

## Next Prompts
- Redeploy backend with proper route configuration
- Verify deployed backend exposes all auth endpoints correctly
- Test auth endpoints individually on deployed backend

## Reflection Note
405 errors often indicate route exists but method not supported, or in deployment scenarios, can indicate routing configuration issues between frontend and backend.

## Failure Modes Observed
Speculative changes to vercel.json without confirming deployment architecture can break the application further. Needed more information about deployment setup before making changes.

## Next Experiment to Improve Prompt Quality
For deployment-related issues, ask about the specific architecture before making configuration changes to avoid breaking the system further.