# Quick Verification Script for Phase 3 Task Management Fix

## What Was Fixed

Two critical configuration issues were preventing task management from working:

### 1. Frontend .env Port Mismatch ✅ FIXED
- **Before**: `VITE_API_BASE_URL=http://localhost:8000`
- **After**: `VITE_API_BASE_URL=http://localhost:8001`

### 2. Vite Proxy Configuration ✅ FIXED
- **Before**: All proxies pointed to `http://localhost:8000`
- **After**: All proxies now point to `http://localhost:8001`

## Quick Start (3 Steps)

### Terminal 1 - Start Backend:
```bash
cd phase_3/backend
python run_server.py
```
Should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8001
```

### Terminal 2 - Start Frontend:
```bash
cd phase_3/frontend
npm run dev
```
Should see:
```
Local:        http://localhost:5173/
```

### Browser - Test:
1. Open http://localhost:5173
2. Login with any email/password (bypass mode)
3. Navigate to "Tasks" tab
4. Try adding a task - it should now work!
5. Try adding/editing/deleting tasks

## Expected Working Features

### Manual Task Management:
- ✅ Add new tasks
- ✅ Edit task details
- ✅ Mark tasks as complete
- ✅ Delete tasks

### Chatbot Task Management:
- ✅ Ask to "add a task"
- ✅ Ask to "list my tasks"
- ✅ Ask to "complete task X"
- ✅ Ask to "delete task X"

## If Still Not Working

1. **Check ports in browser console** (F12):
   - Should not see "Connection refused" errors
   - Should not see "Failed to fetch" with port 8000

2. **Verify files were updated**:
   - `frontend/.env` line should say: `VITE_API_BASE_URL=http://localhost:8001`
   - `frontend/vite.config.js` proxy section should have all targets as `http://localhost:8001`

3. **Clear browser cache**:
   - Restart browser or open in incognito mode
   - Frontend code might be cached

4. **Restart dev servers**:
   - Stop backend and frontend
   - Clear `node_modules/.vite` cache if exists
   - Restart both servers

5. **Check backend logs**:
   - Should see requests being received at port 8001
   - Look for task-related endpoints being called

## Common Error Messages & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| "Connection refused" | Port 8000 still being used | Verify port in .env is 8001 |
| "Failed to fetch" | Backend not running | Start backend on port 8001 |
| "CORS error" | Frontend can't reach backend | Verify proxy in vite.config.js |
| Tasks won't load | Authentication token issue | Logout and login again |

## Architecture

```
Frontend (Port 5173)
    ↓
Vite Dev Proxy (localhost:8001)
    ↓
Backend FastAPI (Port 8001)
    ↓
Database (Neon PostgreSQL or local SQLite)
```

The issue was the proxy pointing to the wrong port, breaking this chain!

