---
id: 2
title: Fix Vercel Auth 405 Errors
stage: refactor
date_iso: 2026-01-23
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: unknown
command: manual
labels: ["vercel", "authentication", "405-error", "fastapi", "refactor"]
links_spec: null
links_ticket: null
links_adr: null
links_pr: null
files_yaml: |
  - frontend/src/config/betterAuthClient.js
tests_yaml: |
  - none
---

# Fix Vercel Auth 405 Errors

## Prompt Text
```
im facing this issue api/auth/sign-in/email:1  Failed to load resource: the server responded with a status of 405 ()
on vercel frontend
```

## Response Text
Fixed 405 errors on Vercel deployment by updating the frontend authentication client to use FastAPI backend endpoints instead of Better Auth endpoints, since Better Auth server wasn't deployed to Vercel.

## Context
User experienced HTTP 405 errors when trying to access authentication endpoints on Vercel deployment. The frontend was trying to reach Better Auth endpoints (/api/auth/sign-up, /api/auth/sign-in/email) that don't exist on the deployed Vercel backend.

## Outcome Impact
- Resolved 405 Method Not Allowed errors for authentication on Vercel
- Updated frontend to use FastAPI backend auth endpoints instead of Better Auth
- Maintained same interface so no changes needed in other frontend components
- Authentication should now work on Vercel deployment

## Technical Details
- Changed frontend auth client from Better Auth endpoints to FastAPI backend endpoints
- Updated endpoints from /api/auth/sign-up, /api/auth/sign-in/email to /auth/register, /auth/login
- Modified authentication flow to work with JWT tokens in localStorage
- Kept same function signatures so existing code continues to work

## Tests Summary
none

## Files Summary
- frontend/src/config/betterAuthClient.js - Updated to use FastAPI backend endpoints

## Next Prompts
none

## Reflection Note
When deploying to platforms like Vercel, ensure all required backend services are properly deployed and accessible, or adapt the frontend to use available endpoints.

## Failure Modes Observed
None - the fix addresses the core issue of unavailable authentication endpoints on Vercel.

## Next Experiment to Improve Prompt Quality
N/A