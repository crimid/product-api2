import time
import logging
import platform
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from logging.handlers import RotatingFileHandler
import os
import psutil
from sqlmodel import SQLModel

from app.database.session import engine, get_session
from app.database import models
from app.routers import auth, products, users

# Create tables
SQLModel.metadata.create_all(engine)

# Configure logging
LOG_FILE = os.getenv("LOG_FILE", "app.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        RotatingFileHandler(LOG_FILE, maxBytes=10485760, backupCount=5),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize app
app = FastAPI(
    title="Product API",
    description="A RESTful API for product management",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Start time for uptime tracking
start_time = time.time()

# Logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time_request = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time_request
    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.3f}s"
    )
    return response

# Include routers
app.include_router(auth.router, tags=["Authentication"])
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(users.router, prefix="/users", tags=["Users"])

# Health check endpoint
@app.get("/health")
def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "uptime": time.time() - start_time,
        "system": {
            "platform": platform.platform(),
            "python": platform.python_version()
        }
    }

# Metrics endpoint
@app.get("/metrics")
def get_metrics():
    """Metrics endpoint for monitoring."""
    return {
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage("/").percent
    }

@app.get("/")
def root():
    return {
        "message": "Welcome to Product API",
        "docs": "/docs",
        "health": "/health"
    }
