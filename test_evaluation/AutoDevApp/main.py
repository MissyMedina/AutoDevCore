"""
AutoDevApp - AutoDevCore Generated App
AutoDevCore Generated Application with Security Features
"""

import uvicorn
from api.routes import router
from config.security import settings
from database import engine, get_db
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from middleware.security import setup_security_middleware
from models import Base
from sqlalchemy.orm import Session

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AutoDevApp", description="AutoDevCore Generated App", version="1.0.0"
)

# Setup security middleware
setup_security_middleware(app)

# CORS is handled by security middleware with proper configuration
# No need to add CORS middleware here as it's included in setup_security_middleware()

# Include API routes
app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to AutoDevApp",
        "description": "AutoDevCore Generated App",
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "AutoDevApp"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
