# Frontend-Backend-Database Connection Fix Guide

This guide addresses the connection issues between the frontend, backend, and database in the Todo AI Chatbot application.

## Problem Identification

1. **Frontend-Backend Mismatch**: The frontend is configured to connect to a production backend URL instead of the local backend
2. **Startup Sequence**: Services need to be started in the correct order
3. **Environment Consistency**: Multiple environment files may have inconsistent configurations

## Solution Steps

### Step 1: Update Frontend Environment Configuration

Update the frontend environment file to connect to the local backend:

```bash
# In frontend/.env, change:
VITE_API_BASE_URL=https://hackathon-2-phase-3-backend.vercel.app

# To:
VITE_API_BASE_URL=http://localhost:8001
```

### Step 2: Verify Backend Startup

The backend is already configured correctly to run on port 8001:

```bash
# In backend/run_server.py
uvicorn.run("src.api.main:app", host="0.0.0.0", port=8001, reload=True)
```

### Step 3: Proper Service Startup Sequence

Start the services in the following order:

1. **Start Better Auth Server** (needed for authentication):
   ```bash
   npm start
   ```
   This starts the Better Auth server on port 3000.

2. **Start Backend Server**:
   ```bash
   cd backend && python run_server.py
   ```
   This starts the FastAPI backend on port 8001.

3. **Start Frontend**:
   ```bash
   cd frontend && npm run dev
   ```
   This starts the React frontend on port 5173.

### Step 4: Verify Database Connection

Test the database connection:

```bash
cd backend && python -c "
from src.database.connection import get_engine
engine = get_engine()
conn = engine.connect()
print('✓ Database connection successful')
conn.close()
"
```

### Step 5: Alternative Startup Method

You can also use the concurrent startup method from the root:

```bash
npm run dev-all
```

This will start both the Better Auth server and the backend simultaneously using:
```json
"dev-all": "concurrently \"npm run dev\" \"cd backend && uvicorn src.api.main:app --reload --port 8001\""
```

### Step 6: Verify API Endpoints

Once all services are running, verify the endpoints:

- Better Auth: `http://localhost:3000/api/auth` (should return auth endpoints)
- Backend API: `http://localhost:8001/` (should return API info)
- Backend Health: `http://localhost:8001/health` (should return health status)
- Frontend: `http://localhost:5173/` (should load the React app)

### Step 7: Troubleshooting

If you still have connection issues:

1. **Check if ports are available**:
   ```bash
   netstat -an | findstr :3000
   netstat -an | findstr :8001
   netstat -an | findstr :5173
   ```

2. **Check CORS configuration** in `backend/src/api/main.py`:
   - Ensure `http://localhost:5173` is in the allowed origins list

3. **Verify environment variables**:
   - Root `.env`: Contains database URL and API keys
   - Frontend `.env`: Has correct `VITE_API_BASE_URL`

4. **Test API manually**:
   ```bash
   curl -X GET http://localhost:8001/
   ```

## Additional Notes

- The application uses a hybrid authentication system supporting both custom JWT and Better Auth JWT
- The database is configured to use NeonDB PostgreSQL with proper SSL settings
- The backend includes proper CORS middleware to allow communication with the frontend
- Both local SQLite and PostgreSQL databases are supported with fallback logic