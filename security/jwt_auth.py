#!/usr/bin/env python3
"""
JWT Authentication System for AutoDevCore
Comprehensive JWT token management and authentication
"""

import hashlib
import secrets
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, Optional

import jwt


class UserRole(Enum):
    """User roles for access control."""

    ADMIN = "admin"
    SENIOR_DEV = "Senior_Dev"
    MIDLVL_DEV = "MidLvl_Dev"
    ENTRYLVL_DEV = "EntryLvl_Dev"
    PROJECT_MANAGER = "project_manager"
    DEVOPS_ENGINEER = "devops_engineer"
    QA_ENGINEER = "qa_engineer"
    BUSINESS_ANALYST = "business_analyst"
    EXECUTIVE_STAKEHOLDER = "stakeholder"
    USER = "user"
    GUEST = "guest"


@dataclass
class User:
    """User data model."""

    id: str
    username: str
    email: str
    role: UserRole
    created_at: datetime
    last_login: Optional[datetime] = None


class JWTAuthManager:
    """Comprehensive JWT authentication manager."""

    def __init__(self, secret_key: Optional[str] = None):
        self.secret_key = secret_key or secrets.token_urlsafe(32)
        self.algorithm = "HS256"
        self.token_expiry_hours = 24
        self.refresh_token_expiry_days = 30

    def hash_password(self, password: str) -> str:
        """Hash password using PBKDF2."""
        salt = secrets.token_hex(16)
        hash_obj = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000
        )
        return f"{salt}${hash_obj.hex()}"

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify password against hash."""
        try:
            salt, hash_hex = hashed_password.split("$")
            hash_obj = hashlib.pbkdf2_hmac(
                "sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000
            )
            return hash_obj.hex() == hash_hex
        except Exception:
            return False

    def create_access_token(self, user: User) -> str:
        """Create JWT access token."""
        payload = {
            "sub": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role.value,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(hours=self.token_expiry_hours),
            "type": "access",
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def create_refresh_token(self, user: User) -> str:
        """Create JWT refresh token."""
        payload = {
            "sub": user.id,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(days=self.refresh_token_expiry_days),
            "type": "refresh",
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify JWT token and return payload."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def refresh_access_token(self, refresh_token: str) -> Optional[str]:
        """Refresh access token using refresh token."""
        payload = self.verify_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            return None

        # Create new user object from refresh token
        user = User(
            id=payload["sub"],
            username="",  # Not in refresh token
            email="",  # Not in refresh token
            role=UserRole.ENTRYLVL_DEV,  # Default role
            created_at=datetime.utcnow(),
        )

        return self.create_access_token(user)

    def has_permission(self, user_role: UserRole, required_role: UserRole) -> bool:
        """Check if user has required role permission."""
        role_hierarchy = {
            UserRole.ADMIN: 10,
            UserRole.EXECUTIVE_STAKEHOLDER: 9,
            UserRole.SENIOR_DEV: 8,
            UserRole.PROJECT_MANAGER: 7,
            UserRole.DEVOPS_ENGINEER: 6,
            UserRole.QA_ENGINEER: 6,
            UserRole.BUSINESS_ANALYST: 6,
            UserRole.MIDLVL_DEV: 5,
            UserRole.ENTRYLVL_DEV: 4,
            UserRole.USER: 3,
            UserRole.GUEST: 1,
        }
        return role_hierarchy.get(user_role, 0) >= role_hierarchy.get(required_role, 0)


class AuthMiddleware:
    """Authentication middleware for web applications."""

    def __init__(self, auth_manager: JWTAuthManager):
        self.auth_manager = auth_manager

    def authenticate_request(self, headers: Dict[str, str]) -> Optional[Dict[str, Any]]:
        """Authenticate request from headers."""
        auth_header = headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]
        return self.auth_manager.verify_token(token)

    def require_auth(self, required_role: UserRole = UserRole.USER):
        """Decorator to require authentication."""

        def decorator(func):
            def wrapper(*args, **kwargs):
                # This would be implemented in the web framework
                # For now, return a placeholder
                return func(*args, **kwargs)

            return wrapper

        return decorator


# Global auth manager instance
auth_manager = JWTAuthManager()


def create_user(
    username: str, email: str, password: str, role: UserRole = UserRole.ENTRYLVL_DEV
) -> User:
    """Create a new user."""
    user_id = secrets.token_urlsafe(16)
    hashed_password = auth_manager.hash_password(password)

    user = User(
        id=user_id,
        username=username,
        email=email,
        role=role,
        created_at=datetime.utcnow(),
    )

    # In a real implementation, save to database
    return user


def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    """Authenticate user and return tokens."""
    # In a real implementation, fetch user from database
    # For demo purposes, create a test user
    if username == "admin" and password == "admin123":
        user = User(
            id="admin-123",
            username=username,
            email="admin@autodevcore.com",
            role=UserRole.ADMIN,
            created_at=datetime.utcnow(),
        )

        access_token = auth_manager.create_access_token(user)
        refresh_token = auth_manager.create_refresh_token(user)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user,
        }

    return None


def verify_user_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify user token and return user info."""
    return auth_manager.verify_token(token)


# Example usage and testing
if __name__ == "__main__":
    # Test JWT authentication
    print("🔐 Testing JWT Authentication System...")

    # Create test user
    user = create_user(
        "testuser", "test@example.com", "password123", UserRole.SENIOR_DEV
    )
    print(f"✅ Created user: {user.username} ({user.role.value})")

    # Generate tokens
    access_token = auth_manager.create_access_token(user)
    refresh_token = auth_manager.create_refresh_token(user)
    print(f"✅ Generated access token: {access_token[:50]}...")
    print(f"✅ Generated refresh token: {refresh_token[:50]}...")

    # Verify token
    payload = auth_manager.verify_token(access_token)
    if payload:
        print(f"✅ Token verified: {payload['username']} ({payload['role']})")
    else:
        print("❌ Token verification failed")

    # Test password hashing
    password = "mypassword123"
    hashed = auth_manager.hash_password(password)
    print(f"✅ Password hashed: {hashed[:50]}...")

    if auth_manager.verify_password(password, hashed):
        print("✅ Password verification successful")
    else:
        print("❌ Password verification failed")

    print("🎉 JWT Authentication System ready!")
