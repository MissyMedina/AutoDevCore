"""
AutoDevApp - simple todo app
AutoDevCore Generated Application
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uvicorn

from database import get_db, engine
from models import Base
from api.routes import router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AutoDevApp",
    description="simple todo app",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to AutoDevApp", "description": "simple todo app"}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "AutoDevApp"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
