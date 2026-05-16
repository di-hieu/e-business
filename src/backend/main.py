"""
SC Chatbot Main Application Entry Point

FastAPI application for Social Commerce AI Chatbot platform.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="SC Chatbot API",
    description="Social Commerce AI Chatbot API for SMEs",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"],
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "debug": str(exc)},
    )


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "SC Chatbot API",
        "version": "1.0.0",
        "status": "running",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "sc-chatbot"}


@app.get("/metrics")
async def metrics():
    """Basic metrics endpoint."""
    return {
        "requests_total": 0,
        "requests_success": 0,
        "requests_error": 0,
    }


# Mount static files
static = StaticFiles(directory=str(Path(__file__).parent.parent / "frontend" / "dist"))

@app.get("/static/{path:path}")
async def serve_static(path: str):
    """Serve static files."""
    return static.dispatch(request, path)


# Import and include API routes
from api import api_router
app.include_router(api_router, prefix="/api")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)