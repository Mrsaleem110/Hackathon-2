# Vercel-optimized API with simple, importable components
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os

# Create app instance
app = FastAPI(
    title="AI-Powered Todo Chatbot API - Vercel Optimized",
    description="Lightweight version optimized for Vercel serverless functions",
    version="1.0.0"
)

# Simple CORS setup
cors_origins = [
    "http://localhost:5173", "http://localhost:3000", "http://localhost:8000",
    "http://127.0.0.1:5173", "http://127.0.0.1:3000", "http://127.0.0.1:8000",
    "https://hackathon-2-p-3-frontend.vercel.app",
    "https://hackathon-2-p-3-backend.vercel.app",
    os.getenv("FRONTEND_URL", "https://hackathon-2-p-3-frontend.vercel.app")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define routes as functions that can be imported
def api_health():
    return {"status": "operational", "service": "api", "vercel_optimized": True}

def catch_all_handler(path_name: str):
    return {
        "status": "info",
        "message": f"Route '/{path_name}' is not yet implemented in Vercel-optimized mode",
        "hint": "This is a lightweight version optimized for Vercel deployment"
    }

# Add routes to the app
@app.get("/api/health")
def health_endpoint():
    return api_health()

@app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"])
async def catch_all_endpoint(path_name: str):
    return catch_all_handler(path_name)