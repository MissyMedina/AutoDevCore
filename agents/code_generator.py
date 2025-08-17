"""
Code Generator Agent - Generates application codebase with security features
"""

from pathlib import Path
from typing import Any, Dict

from .security_generator import SecurityGeneratorAgent

class CodeGeneratorAgent:
    """Agent responsible for generating the application codebase."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.security_generator = SecurityGeneratorAgent(verbose)

    def generate_codebase(
        self, app_plan: Dict[str, Any], app_dir: Path
    ) -> Dict[str, str]:
        """
        Generate a complete codebase based on the app plan.

        Args:
            app_plan: The app plan from the composer agent
            app_dir: The directory where to generate the codebase

        Returns:
            Dictionary containing file paths and content
        """
        if self.verbose:
            print(
                f"[CodeGeneratorAgent] Generating codebase for: {app_plan.get('app_name', 'AutoDevApp')}"
            )

        tech_stack = app_plan.get("tech_stack", {})
        backend = tech_stack.get("backend", "Python/FastAPI")
        idea = app_plan.get("description", "AutoDevCore Generated App")

        if "python" in backend.lower() or "fastapi" in backend.lower():
            return self._generate_python_codebase(idea, app_plan)
        elif "node" in backend.lower() or "javascript" in backend.lower():
            return self._generate_node_codebase(idea, app_plan)
        else:
            return self._generate_python_codebase(idea, app_plan)  # Default to Python

    def _generate_python_codebase(
        self, idea: str, app_plan: Dict[str, Any]
    ) -> Dict[str, str]:
        """Generate a Python/FastAPI codebase with security features."""

        # Generate base codebase
        base_files = {
            "main.py": self._generate_main_py(idea, app_plan),
            "models.py": self._generate_models_py(app_plan),
            "database.py": self._generate_database_py(app_plan),
            "api/routes.py": self._generate_routes_py(app_plan),
            "api/__init__.py": "",
            "utils/helpers.py": self._generate_helpers_py(),
            "utils/__init__.py": "",
            "tests/test_main.py": self._generate_tests_py(app_plan),
            "tests/__init__.py": "",
            "config.py": self._generate_config_py(),
            "requirements.txt": self._generate_requirements_txt(),
            ".env.example": self._generate_env_example(),
            "Dockerfile": self._generate_dockerfile(),
            ".gitignore": self._generate_gitignore(),
        }

        # Generate security features
        security_files = self.security_generator.generate_security_features(app_plan)

        # Merge base and security files
        all_files = {**base_files, **security_files}

        return all_files

    def _generate_node_codebase(
        self, idea: str, app_plan: Dict[str, Any]
    ) -> Dict[str, str]:
        """Generate a Node.js/Express codebase."""

        return {
            "index.js": self._generate_index_js(idea, app_plan),
            "package.json": self._generate_package_json(idea, app_plan),
            "models/User.js": self._generate_user_model_js(),
            "routes/api.js": self._generate_api_routes_js(app_plan),
            "utils/helpers.js": self._generate_helpers_js(),
            "tests/test.js": self._generate_tests_js(app_plan),
            ".env.example": self._generate_env_example(),
            "Dockerfile": self._generate_dockerfile(),
            ".gitignore": self._generate_gitignore(),
        }

    def _generate_main_py(self, idea: str, app_plan: Dict[str, Any]) -> str:
        """Generate the main FastAPI application file."""

        app_name = app_plan.get("name", "AutoDevApp")

        return f'''"""
{app_name} - {idea}
AutoDevCore Generated Application with Security Features
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uvicorn

from database import get_db, engine
from models import Base
from api.routes import router
from middleware.security import setup_security_middleware
from config.security import settings

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="{app_name}",
    description="{idea}",
    version="1.0.0"
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
    return {{"message": "Welcome to {app_name}", "description": "{idea}"}}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {{"status": "healthy", "service": "{app_name}"}}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''

    def _generate_models_py(self, app_plan: Dict[str, Any]) -> str:
        """Generate the SQLAlchemy models."""

        models_content = '''"""
SQLAlchemy Models
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    """User model."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
'''

        # Add specific models based on app type
        idea_lower = app_plan.get("description", "").lower()
        if any(word in idea_lower for word in ["inventory", "stock"]):
            models_content += '''

class Product(Base):
    """Product model for inventory management."""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(DECIMAL(10, 2))
    stock_quantity = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
'''

        return models_content

    def _generate_database_py(self, app_plan: Dict[str, Any]) -> str:
        """Generate the database configuration."""

        return '''"""
Database Configuration
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# Database URL - use environment variable or default to SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
'''

    def _generate_routes_py(self, app_plan: Dict[str, Any]) -> str:
        """Generate the API routes."""

        routes_content = '''"""
API Routes with Input Validation
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel, validator, Field
from database import get_db
from models import User
from utils.validation import validate_password_strength

# Pydantic models for input validation
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Username must be 3-50 characters")
    email: str = Field(..., description="Valid email address")
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")

    @validator('email')
    def validate_email(cls, v):

        import re
        if not re.match(r"[^@]+@[^@]+\\.[^@]+", v):
            raise ValueError('Invalid email format')
        return v

    @validator('password')
    def validate_password(cls, v):
        if not validate_password_strength(v):
            raise ValueError('Password does not meet security requirements')
        return v

class UserUpdate(BaseModel):
    username: str = Field(None, min_length=3, max_length=50)
    email: str = Field(None)
    is_active: bool = Field(None)

    @validator('email')
    def validate_email(cls, v):
        if v is not None:

            import re
            if not re.match(r"[^@]+@[^@]+\.[^@]+", v):
                raise ValueError('Invalid email format')
        return v

router = APIRouter()

@router.post("/users/", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user with validation."""
    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )

    # Create new user (password hashing would be handled in auth system)
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password="hashed_password_here"  # Would be hashed in real implementation
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully", "user_id": new_user.id}

@router.get("/users/", response_model=List[dict])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all users."""
    users = db.query(User).offset(skip).limit(limit).all()
    return [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active,
            "created_at": user.created_at
        }
        for user in users
    ]

@router.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user by ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_active": user.is_active,
        "created_at": user.created_at
    }
'''

        # Add product routes if it's an inventory app
        idea_lower = app_plan.get("description", "").lower()
        if any(word in idea_lower for word in ["inventory", "stock"]):
            routes_content += '''

@router.get("/products/", response_model=List[dict])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all products."""

    from models import Product
    products = db.query(Product).offset(skip).limit(limit).all()
    return [
        {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": float(product.price) if product.price else None,
            "stock_quantity": product.stock_quantity,
            "created_at": product.created_at
        }
        for product in products
    ]

@router.get("/products/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get product by ID."""

    from models import Product
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": float(product.price) if product.price else None,
        "stock_quantity": product.stock_quantity,
        "created_at": product.created_at
    }
'''

        return routes_content

    def _generate_helpers_py(self) -> str:
        """Generate utility helper functions."""

        return '''"""
Utility Helper Functions
"""

import hashlib
import secrets
from datetime import datetime

def hash_password(password: str) -> str:
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_token() -> str:
    """Generate a random token."""
    return secrets.token_urlsafe(32)

def format_datetime(dt: datetime) -> str:
    """Format datetime for API responses."""
    return dt.isoformat() if dt else None
'''

    def _generate_tests_py(self, app_plan: Dict[str, Any]) -> str:
        """Generate test files."""

        app_name = app_plan.get("name", "AutoDevApp")

        return f'''"""
Tests for {app_name}
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_get_users():
    """Test the users endpoint."""
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
'''

    def _generate_config_py(self) -> str:
        """Generate configuration file."""

        return '''"""
Application Configuration
"""

import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings."""
    app_name: str = "AutoDevApp"
    debug: bool = False
    database_url: str = "sqlite:///./app.db"
    secret_key: str = "your-secret-key-here"

    class Config:
        env_file = ".env"

settings = Settings()
'''

    def _generate_requirements_txt(self) -> str:
        """Generate requirements.txt with security dependencies."""

        return """# Core Dependencies
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
python-dotenv==1.0.0

# Security Dependencies
passlib[bcrypt]==1.7.4
python-jose[cryptography]==3.3.0
python-multipart==0.0.6
slowapi==0.1.9
pydantic[email]==2.5.0
pydantic-settings==2.1.0
cryptography==41.0.7

# Development Dependencies
pytest==7.4.3
pytest-cov==4.1.0
black==23.11.0
flake8==6.1.0
"""

    def _generate_env_example(self) -> str:
        """Generate secure environment variables example."""

        return """# Environment Variables Example
# Copy this file to .env and update the values

# Database Configuration
DATABASE_URL=sqlite:///./app.db

# Security Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Configuration
CORS_ORIGINS=["http://localhost:3000", "https://yourdomain.com"]
ALLOWED_HOSTS=["localhost", "127.0.0.1", "yourdomain.com"]

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60

# Password Policy
MIN_PASSWORD_LENGTH=8
REQUIRE_UPPERCASE=true
REQUIRE_LOWERCASE=true
REQUIRE_NUMBERS=true
REQUIRE_SPECIAL_CHARS=false

# Application Configuration
DEBUG=false
APP_NAME=AutoDevApp

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Security Headers
ENABLE_HTTPS_REDIRECT=false
ENABLE_HSTS=true
ENABLE_CSP=true
"""

    def _generate_dockerfile(self) -> str:
        """Generate Dockerfile."""

        return """# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "main.py"]
"""

    def _generate_gitignore(self) -> str:
        """Generate .gitignore file."""

        return """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Environment variables
.env

# Database
*.db
*.sqlite

# Logs
*.log

# OS
.DS_Store
Thumbs.db
"""

    def _generate_index_js(self, idea: str, app_plan: Dict[str, Any]) -> str:
        """Generate the main Node.js application file."""

        app_name = app_plan.get("name", "AutoDevApp")

        return f"""/**
 * {app_name} - {idea}
 * AutoDevCore Generated Application
 */

const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');

// Load environment variables
dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Routes
app.get('/', (req, res) => {{
    res.json({{
        message: 'Welcome to {app_name}',
        description: '{idea}'
    }});
}});

app.get('/health', (req, res) => {{
    res.json({{
        status: 'healthy',
        service: '{app_name}'
    }});
}});

// API routes
app.use('/api/v1', require('./routes/api'));

// Error handling middleware
app.use((err, req, res, next) => {{
    console.error(err.stack);
    res.status(500).json({{ error: 'Something went wrong!' }});
}});

app.listen(PORT, () => {{
    console.log(`{app_name} server running on port ${{PORT}}`);
}});
"""

    def _generate_package_json(self, idea: str, app_plan: Dict[str, Any]) -> str:
        """Generate package.json for Node.js app."""

        app_name = app_plan.get("name", "AutoDevApp")

        return f"""{{
  "name": "{app_name.lower().replace(' ', '-')}",
  "version": "1.0.0",
  "description": "{idea}",
  "main": "index.js",
  "scripts": {{
    "start": "node index.js",
    "dev": "nodemon index.js",
    "test": "jest"
  }},
  "dependencies": {{
    "express": "^4.18.2",
    "cors": "^2.8.5",
    "dotenv": "^16.3.1"
  }},
  "devDependencies": {{
    "nodemon": "^3.0.2",
    "jest": "^29.7.0"
  }},
  "keywords": ["autodevcore", "generated"],
  "author": "AutoDevCore",
  "license": "MIT"
}}
"""

    def _generate_user_model_js(self) -> str:
        """Generate User model for Node.js."""

        return """/**
 * User Model
 */

class User {
    constructor(id, username, email, isActive = true, createdAt = new Date()) {
        this.id = id;
        this.username = username;
        this.email = email;
        this.isActive = isActive;
        this.createdAt = createdAt;
    }

    toJSON() {
        return {
            id: this.id,
            username: this.username,
            email: this.email,
            isActive: this.isActive,
            createdAt: this.createdAt
        };
    }
}

module.exports = User;
"""

    def _generate_api_routes_js(self, app_plan: Dict[str, Any]) -> str:
        """Generate API routes for Node.js."""

        return """/**
 * API Routes
 */

const express = require('express');
const router = express.Router();

// Mock data - in production, use a database
let users = [
    {
        id: 1,
        username: 'admin',
        email: 'admin@example.com',
        isActive: true,
        createdAt: new Date()
    }
];

// Get all users
router.get('/users', (req, res) => {
    res.json(users);
});

// Get user by ID
router.get('/users/:id', (req, res) => {
    const user = users.find(u => u.id === parseInt(req.params.id));
    if (!user) {
        return res.status(404).json({ error: 'User not found' });
    }
    res.json(user);
});

module.exports = router;
"""

    def _generate_helpers_js(self) -> str:
        """Generate helper functions for Node.js."""

        return """/**
 * Utility Helper Functions
 */

const crypto = require('crypto');

function hashPassword(password) {
    return crypto.createHash('sha256').update(password).digest('hex');
}

function generateToken() {
    return crypto.randomBytes(32).toString('hex');
}

function formatDate(date) {
    return date.toISOString();
}

module.exports = {
    hashPassword,
    generateToken,
    formatDate
};
"""

    def _generate_tests_js(self, app_plan: Dict[str, Any]) -> str:
        """Generate tests for Node.js app."""

        app_name = app_plan.get("name", "AutoDevApp")

        return f"""/**
 * Tests for {app_name}
 */

const request = require('supertest');
const app = require('../index');

describe('API Tests', () => {{
    test('GET / should return welcome message', async () => {{
        const response = await request(app).get('/');
        expect(response.status).toBe(200);
        expect(response.body.message).toBe('Welcome to {app_name}');
    }});

    test('GET /health should return health status', async () => {{
        const response = await request(app).get('/health');
        expect(response.status).toBe(200);
        expect(response.body.status).toBe('healthy');
    }});

    test('GET /api/v1/users should return users', async () => {{
        const response = await request(app).get('/api/v1/users');
        expect(response.status).toBe(200);
        expect(Array.isArray(response.body)).toBe(true);
    }});
}});
"""
