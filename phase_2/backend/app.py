from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import users, items, auth
from app.database_init import create_db_and_tables
import os

# Create FastAPI app instance
app = FastAPI(
    title="Next.js/FastAPI Application API",
    description="API for the full-stack Next.js/FastAPI application",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Hugging Face Spaces URLs
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

@app.on_event("startup")
async def on_startup():
    create_db_and_tables()

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "API is running"}

# For Hugging Face Space
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 7860)))