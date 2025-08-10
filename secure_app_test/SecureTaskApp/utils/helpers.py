"""
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
