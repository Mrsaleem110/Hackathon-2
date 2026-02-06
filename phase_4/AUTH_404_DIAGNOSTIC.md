# Troubleshooting: auth/login:1 404 Error

## What We Know

1. **Backend logs show NO GET requests to /auth/login** - only POST requests
2. **Frontend code is correct** - only makes POST requests to /auth/login, /auth/register
3. **Vite proxy is configured correctly** - only proxies /auth/, /tasks, /chat, /api

## Possible Causes of the 404 Error

### 1. Source Map File Missing
- Error format `auth/login:1` could mean line 1 of auth/login source map
- Browser trying to load `http://localhost:8001/auth/login.js.map`
- This would cause a 404 but NOT break functionality

### 2. Browser Extension or Prefetch
- Some extensions or browser features prefetch pages
- Could be trying to access `/auth/login` as a page URL instead of API

### 3. Relative URL Somewhere
- Check if there's any `fetch('auth/login')` without the leading `/`
- This would be resolved differently

## How to Verify if This Is Actually a Problem

1. **Does signup work?**
   - Go to http://localhost:5173/register
   - Fill in form and click "Sign Up"
   - Do you get redirected to dashboard?
   - Can you see your tasks/stats?

2. **Check Browser Console**
   - Open DevTools (F12)
   - Go to Console tab
   - Do you see any actual errors or just warnings?
   - Network tab - can you see POST /auth/register returning 200?

3. **Check Backend Logs**
   - Start backend with: `python run_server.py`
   - Watch for `GET /auth/login` - should NOT see this
   - Watch for `POST /auth/login` - should see 200 OK

## Solution Approach

The error message might be:
- ✓ **Harmless warning** - app still works perfectly
- ✗ **Actual blocking issue** - signup/login doesn't work

If signup/login IS working (redirects to dashboard, loads tasks, etc.), then this 404 is just a cosmetic warning and can be ignored or investigated later.

If signup/login is NOT working, we need to:
1. Check what actual requests are failing
2. Look at network tab in DevTools
3. Check browser console for JavaScript errors
