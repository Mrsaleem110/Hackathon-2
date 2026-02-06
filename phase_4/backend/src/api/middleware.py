from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import time
import logging
from typing import Callable, Any

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    """Middleware to log incoming requests."""
    def __init__(self, app: FastAPI):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        request = Request(scope)
        start_time = time.time()

        # Log the request
        logger.info(f"Request: {request.method} {request.url}")

        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                # Calculate response time
                process_time = time.time() - start_time
                response_headers = message.get("headers", [])
                response_headers.append((b"x-process-time", str(process_time).encode("latin-1")))
                message["headers"] = response_headers

                # Log the response
                status_code = message["status"]
                logger.info(f"Response: {status_code} in {process_time:.2f}s")

            await send(message)

        return await self.app(scope, receive, send_wrapper)

def add_security_headers(app: FastAPI):
    """Add security headers to responses."""
    @app.middleware("http")
    async def security_headers(request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response

def add_request_id_middleware(app: FastAPI):
    """Add request ID to each request for tracing."""
    @app.middleware("http")
    async def request_id_middleware(request: Request, call_next):
        # Generate a simple request ID
        request_id = f"req-{int(time.time() * 1000000)}"
        request.state.request_id = request_id

        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response