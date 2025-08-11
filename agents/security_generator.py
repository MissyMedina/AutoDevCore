"""
Security Generator Agent - Adds security features to generated applications
"""

from pathlib import Path
from typing import Any, Dict, List


class SecurityGeneratorAgent:
    """Agent responsible for adding security features to generated applications."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.name = "SecurityGenerator"

    def generate_security_features(self, app_plan: Dict[str, Any]) -> Dict[str, str]:
        """Generate security-related files and code."""
        if self.verbose:
            print(f"[{self.name}] Generating security features...")

        return {
            "auth/auth.py": self._generate_auth_system(),
            "auth/models.py": self._generate_auth_models(),
            "auth/dependencies.py": self._generate_auth_dependencies(),
            "middleware/security.py": self._generate_security_middleware(),
            "config/security.py": self._generate_security_config(),
            "utils/validation.py": self._generate_validation_utils(),
            "requirements_security.txt": self._generate_security_requirements(),
        }

    def _generate_auth_system(self) -> str:
        """Generate authentication system."""
        return '''"""
Authentication System
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session

from database import get_db
from models import User
from config.security import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT token handling
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception: HTTPException) -> dict:
    """Verify and decode a JWT token."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return payload
    except JWTError:
        raise credentials_exception

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """Get the current authenticated user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = verify_token(token, credentials_exception)
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get the current active user."""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
'''

    def _generate_auth_models(self) -> str:
        """Generate authentication Pydantic models."""
        return '''"""
Authentication Pydantic Models
"""

from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    """User creation model."""
    username: str
    email: EmailStr
    password: str
    
    @validator('username')
    def validate_username(cls, v):
        if len(v) < 3:
            raise ValueError('Username must be at least 3 characters')
        if len(v) > 50:
            raise ValueError('Username must be less than 50 characters')
        return v
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one number')
        return v

class UserLogin(BaseModel):
    """User login model."""
    username: str
    password: str

class Token(BaseModel):
    """Token response model."""
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    """User response model."""
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
'''

    def _generate_security_middleware(self) -> str:
        """Generate security middleware."""
        return '''"""
Security Middleware
"""

from fastapi import Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from starlette.middleware.base import BaseHTTPMiddleware
import time
import logging

logger = logging.getLogger(__name__)

class SecurityMiddleware(BaseHTTPMiddleware):
    """Custom security middleware."""
    
    async def dispatch(self, request: Request, call_next):
        # Add security headers
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        return response

def setup_security_middleware(app):
    """Setup all security middleware."""
    
    # Rate limiting
    limiter = Limiter(key_func=get_remote_address)
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    
    # CORS with proper configuration from environment
    from config.security import settings
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
    )
    
    # Trusted hosts from environment
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.ALLOWED_HOSTS
    )
    
    # Custom security middleware
    app.add_middleware(SecurityMiddleware)
'''

    def _generate_security_config(self) -> str:
        """Generate security configuration."""
        return '''"""
Security Configuration
"""

from pydantic_settings import BaseSettings
from typing import List
import secrets

class SecuritySettings(BaseSettings):
    """Security settings."""
    
    # JWT Settings
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database Settings
    DATABASE_URL: str = "sqlite:///./app.db"
    
    # Security Settings
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1"]
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Password Settings
    MIN_PASSWORD_LENGTH: int = 8
    REQUIRE_UPPERCASE: bool = True
    REQUIRE_LOWERCASE: bool = True
    REQUIRE_NUMBERS: bool = True
    REQUIRE_SPECIAL_CHARS: bool = False
    
    class Config:
        env_file = ".env"

settings = SecuritySettings()
'''

    def _generate_validation_utils(self) -> str:
        """Generate validation utilities."""
        return '''"""
Validation Utilities
"""

import re
from typing import Any, Dict, List
from fastapi import HTTPException, status

def validate_email(email: str) -> bool:
    """Validate email format."""
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password_strength(password: str) -> Dict[str, Any]:
    """Validate password strength."""
    errors = []
    
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")
    
    if not re.search(r'[A-Z]', password):
        errors.append("Password must contain at least one uppercase letter")
    
    if not re.search(r'[a-z]', password):
        errors.append("Password must contain at least one lowercase letter")
    
    if not re.search(r'\d', password):
        errors.append("Password must contain at least one number")
    
    return {
        "is_valid": len(errors) == 0,
        "errors": errors
    }

def sanitize_input(input_str: str) -> str:
    """Basic input sanitization."""
    # Remove potentially dangerous characters
    dangerous_chars = ['<', '>', '"', "'", '&']
    for char in dangerous_chars:
        input_str = input_str.replace(char, '')
    return input_str.strip()

def validate_request_size(content_length: int, max_size: int = 1024 * 1024) -> bool:
    """Validate request size."""
    return content_length <= max_size
'''

    def _generate_security_requirements(self) -> str:
        """Generate security requirements."""
        return """# Security Dependencies
passlib[bcrypt]==1.7.4
python-jose[cryptography]==3.3.0
python-multipart==0.0.6
slowapi==0.1.9
pydantic[email]==2.5.0
pydantic-settings==2.1.0
cryptography==41.0.7
"""

    def _generate_auth_dependencies(self) -> str:
        """Generate authentication dependencies."""
        return '''"""
Authentication Dependencies
"""

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
from models import User
from auth.auth import get_current_active_user

def require_admin(current_user: User = Depends(get_current_active_user)) -> User:
    """Require admin role."""
    if not hasattr(current_user, 'is_admin') or not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

def require_user_permission(user_id: int, current_user: User = Depends(get_current_active_user)) -> User:
    """Require user to access their own data or be admin."""
    if current_user.id != user_id and not getattr(current_user, 'is_admin', False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    return current_user
'''
