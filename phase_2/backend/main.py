







import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import users, items, auth
from app.config import get_settings

# Import database functions without triggering settings validation at import time
from app.database_init import create_db_and_tables

# Create FastAPI app instance with lifespan to handle startup events properly
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup - only run if settings are available
    try:
        settings = get_settings()  # This will raise an exception if required env vars are missing
        # In serverless environments, avoid heavy initialization during cold start
        # Database initialization should be handled separately or in individual functions
        print("Application startup complete")
    except Exception as e:
        print(f"Warning: Could not initialize during startup: {e}")
        # In serverless environments, database initialization might not be possible during cold start
        pass
    yield
    # Shutdown (if needed)
    print("Application shutdown")

app = FastAPI(
    title="Next.js/FastAPI Application API",
    description="API for the full-stack Next.js/FastAPI application",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")  # Default for local development
vercel_url = os.getenv("VERCEL_URL", "")  # Vercel provides this automatically for deployments
allowed_origins = [frontend_url, "http://localhost:3000", "https://localhost:3000", "http://127.0.0.1:3000", "https://*.vercel.app"]
if vercel_url:
    allowed_origins.append(f"https://{vercel_url}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # Allow your frontend domain and Vercel preview URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(items.router, prefix="/api/v1", tags=["items"])
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Next.js/FastAPI Application API"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "API is running"}

# For Vercel serverless deployment
try:
    # Import for Vercel
    from mangum import Mangum

    # Create the Mangum handler with specific configuration for better performance
    handler = Mangum(app, lifespan="off")
except ImportError:
    # For local development
    import uvicorn
    if __name__ == "__main__":
        port = int(os.getenv("PORT", 8000))
        uvicorn.run(app, host="0.0.0.0", port=port)