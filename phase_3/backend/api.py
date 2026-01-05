import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create FastAPI app with proper structure for your current application
from fastapi import Depends
from sqlmodel import Session
from app.db.database import get_session
from app.api.v1.auth import router as auth_router
from app.chat.routes import router as chat_router
from app.models.conversation import Conversation, Message
from app.models.item import Item, ItemCreate, ItemUpdate, Priority
from app.models.user import User
from sqlmodel import SQLModel
from app.db.database import engine

# Create FastAPI app
app = FastAPI(title="Todo AI Chat API", version="1.0.0")

# Create database tables
@app.on_event("startup")
def on_startup():
    # Import all models to ensure they are registered with SQLModel
    from app.models.conversation import Conversation, Message
    from app.models.item import Item
    from app.models.user import User
    from app.models.session import Session
    from app.models.task import Task
    SQLModel.metadata.create_all(engine)

# Add CORS middleware for deployment
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")  # Default for local development
vercel_url = os.getenv("VERCEL_URL", "")  # Vercel provides this automatically for deployments
allowed_origins = [
    frontend_url,
    "http://localhost:3000",
    "https://localhost:3000",
    "http://127.0.0.1:3000",
    "https://*.vercel.app"
]
if vercel_url:
    allowed_origins.append(f"https://{vercel_url}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # Allow your frontend domain and Vercel preview URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your current API routes
app.include_router(auth_router)
app.include_router(chat_router)

# Health check and root endpoints
@app.get("/")
def read_root():
    return {"message": "Todo AI Chat API is running!"}

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