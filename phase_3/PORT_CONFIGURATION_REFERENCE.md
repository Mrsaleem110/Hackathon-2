# Port Configuration Reference

## Current Setup (CORRECT)

```
Frontend App:              http://localhost:5173
Backend API:               http://localhost:8001
Frontend .env:             VITE_API_BASE_URL=http://localhost:8001
Vite Proxy Config:         target: 'http://localhost:8001'
```

## Before The Fix (BROKEN)

```
Frontend App:              http://localhost:5173
Backend API:               http://localhost:8001
Frontend .env:             VITE_API_BASE_URL=http://localhost:8000  ❌
Vite Proxy Config:         target: 'http://localhost:8000'           ❌
```

---

## Why Port 8001?

The backend server starts on port 8001 via `run_server.py`:
```python
if __name__ == "__main__":
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8001, reload=True)
```

This is hardcoded, so the frontend MUST connect to 8001.

---

## Files That Control Ports

### 1. Backend Port (Can Change)
**File:** `backend/run_server.py`
```python
uvicorn.run("src.api.main:app", host="0.0.0.0", port=8001, reload=True)
                                                  ^^^^
                                                Backend port
```

### 2. Frontend Port (Can Change)
**File:** `frontend/vite.config.js`
```javascript
server: {
  host: true,    // Accessible from outside
  proxy: { ... } // Proxy rules
}
```
The actual port is run via: `npm run dev` (default: 5173)

### 3. Backend URL in Frontend (MUST MATCH Backend Port)
**File:** `frontend/.env`
```dotenv
VITE_API_BASE_URL=http://localhost:8001
                                    ^^^^
                                Must match backend port!
```

### 4. Dev Proxy Rules (MUST MATCH Backend Port)
**File:** `frontend/vite.config.js`
```javascript
proxy: {
  '/tasks': {
    target: 'http://localhost:8001',  // Must match backend port!
    changeOrigin: true,
    secure: false,
  },
  // ... other proxies
}
```

---

## How To Change Ports

### If You Want Backend on Port 8000:
1. Edit `backend/run_server.py`:
   ```python
   uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True)
   ```

2. Update `frontend/.env`:
   ```dotenv
   VITE_API_BASE_URL=http://localhost:8000
   ```

3. Update `frontend/vite.config.js`:
   ```javascript
   target: 'http://localhost:8000'  // For all 5 proxies
   ```

### If You Want Frontend on Port 3000:
1. Start frontend: `npm run dev -- --port 3000`
2. Access at: `http://localhost:3000`
3. No changes needed to backend or .env files!

---

## Environment Variables Used

### Frontend
- `VITE_API_BASE_URL` - Where to send API requests
- `VITE_BETTER_AUTH_URL` - Better Auth server URL
- `NEXT_PUBLIC_OPENAI_API_KEY` - OpenAI API key
- `NEXT_PUBLIC_OPENAI_DOMAIN_KEY` - ChatKit domain key

### Backend
- `DATABASE_URL` - PostgreSQL connection string
- `OPENAI_API_KEY` - OpenAI API key
- `BETTER_AUTH_SECRET` - Auth secret
- `OPENAI_MODEL` - Model to use (default: gpt-3.5-turbo)
- `MCP_SERVER_URL` - MCP server location

---

## Quick Verification

### Check Backend is Running on 8001:
```bash
curl http://localhost:8001/health
# Should return: {"status":"healthy",...}
```

### Check Frontend Config:
```bash
# From frontend directory:
grep VITE_API_BASE_URL .env
# Should output: VITE_API_BASE_URL=http://localhost:8001
```

### Check Vite Proxy:
```bash
# From frontend directory:
grep -A 2 "'/tasks':" vite.config.js
# Should show: target: 'http://localhost:8001'
```

---

## Common Port Issues

| Problem | Check | Solution |
|---------|-------|----------|
| Tasks won't load | Network tab in DevTools | Verify .env has correct port |
| Connection refused | Backend logs | Check backend running on 8001 |
| 404 errors | Frontend console | Verify vite.config.js proxy |
| CORS errors | Browser console | Check CORS in backend |
| Port already in use | Terminal | Kill other process on port |

---

## Port Availability Check

### Check if Port is In Use:

**Windows (PowerShell):**
```powershell
netstat -ano | findstr :8001
netstat -ano | findstr :5173
```

**Mac/Linux:**
```bash
lsof -i :8001
lsof -i :5173
```

---

**Summary:** Frontend (5173) → Vite Proxy (5173) → Backend (8001) → Database

