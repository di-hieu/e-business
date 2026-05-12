"""
SC Chatbot Main Application

FastAPI application for Social Commerce AI Chatbot platform.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
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
    allow_origins=["*"],  # Configure in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"],  # Configure in production
)


@asynccontextmanager
async def lifespan(manager: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Starting SC Chatbot API...")
    yield
    # Shutdown
    logger.info("Shutting down SC Chatbot API...")


app.lifespan = lifespan


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "message": "SC Chatbot API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "sc-chatbot"
    }