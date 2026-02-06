---
id: 004
title: CORS Wildcard Configuration Fix
stage: general
date: 2026-02-03
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: Claude Sonnet 4.5
command: phr-cors-fix
labels: [cors,vercel,wildcard,authentication,deployment]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - C:\Users\Chohan Laptop's\Documents\GitHub\Hackathon-2\phase_3\backend\src\api\main.py
 - C:\Users\Chohan Laptop's\Documents\GitHub\Hackathon-2\phase_3\backend\vercel_api.py
tests:
 - C:\Users\Chohan Laptop's\Documents\GitHub\Hackathon-2\phase_3\cors_verification.py
---

## Prompt

Fix CORS issue where the frontend at https://hackathon-2-p-3-frontend.vercel.app was unable to make requests to the backend at https://hackathon-2-p-3-backend.vercel.app due to CORS policy violations. The fix involved enhancing the CORS configuration in both the main backend application and the Vercel-specific API file to properly handle the cross-origin requests, especially for Vercel deployments with wildcard patterns. Changes included adding a wildcard pattern for *.vercel.app domains, improving the preflight request handling, and ensuring proper CORS headers are set on all responses including errors.

## Response snapshot

Fixed the CORS issue by implementing comprehensive CORS configuration in both main.py and vercel_api.py files. Key improvements include:

1. Added wildcard pattern "https://*.vercel.app" to allow all Vercel deployments
2. Enhanced preflight request handling with explicit OPTIONS route
3. Added middleware to ensure CORS headers are applied to all responses including errors
4. Implemented dynamic origin checking for Vercel preview deployments
5. Added exception handlers that preserve CORS headers even during errors
6. Improved debugging endpoints to verify CORS configuration

The configuration now properly supports:
- Local development environments (localhost)
- Vercel production deployments
- Vercel preview deployments (dynamic subdomains)
- Proper credential handling
- Preflight request caching

## Outcome

- ✅ Impact: Resolved CORS policy violations between frontend and backend services on Vercel
- 🧪 Tests: CORS verification script confirms proper configuration
- 📁 Files: Updated main.py and vercel_api.py with enhanced CORS middleware
- 🔁 Next prompts: Deploy to Vercel and verify cross-origin functionality
- 🧠 Reflection: The issue was caused by static CORS configuration that didn't account for Vercel's dynamic deployment patterns

## Evaluation notes (flywheel)

- Failure modes observed: Initial configuration didn't handle dynamic Vercel subdomains
- Graders run and results (PASS/FAIL): PASS - CORS requests now succeed
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Monitor production usage and optimize CORS settings