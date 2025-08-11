"""
AutoDevApp - simple todo app
AutoDevCore Generated Application
"""

import uvicorn
from api.routes import router
from database import engine, get_db
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import Base
from sqlalchemy.orm import Session

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AutoDevApp", description="simple todo app", version="1.0.0")

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
