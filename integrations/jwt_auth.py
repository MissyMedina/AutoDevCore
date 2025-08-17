#!/usr/bin/env python3
"""
AutoDevCore JWT Authentication System
Provides secure authentication for API endpoints and user sessions
"""

import datetime
import hashlib
import json
import os
import secrets
from pathlib import Path
from typing import Any, Dict, Optional, Union

import jwt


class JWTAuthManager:
    """JWT Authentication Manager for AutoDevCore"""

    def __init__(
        self,
        secret_key: Optional[str] = None,
        config_file: str = "config/auth_config.json",
    ):
        self.config_file = Path(config_file)
        self.config_file.parent.mkdir(exist_ok=True)

        # Generate or load secret key
        if secret_key:
            self.secret_key = secret_key
        else:
            self.secret_key = self._load_or_generate_secret_key()

        # JWT configuration
        self.algorithm = "HS256"
        self.expiration_hours = 24
        self.refresh_expiration_days = 30

        # Load user database
        self.users = self._load_users()

    def _load_or_generate_secret_key(self) -> str:
        """Load existing secret key or generate a new one"""
        if self.config_file.exists():
            try:
                with open(self.config_file, "r") as f:
                    config = json.load(f)
                    return config.get("secret_key", self._generate_secret_key())
            except Exception:
                pass

        # Generate new secret key
        secret_key = self._generate_secret_key()
        self._save_config({"secret_key": secret_key})
        return secret_key

    def _generate_secret_key(self) -> str:
        """Generate a secure secret key"""
        return secrets.token_urlsafe(32)

    def _save_config(self, config: Dict[str, Any]):
        """Save configuration to file"""
        try:
            with open(self.config_file, "w") as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save auth config: {e}")

    def _load_users(self) -> Dict[str, Dict[str, Any]]:
        """Load user database"""
        users_file = Path("config/users.json")
        if users_file.exists():
            try:
                with open(users_file, "r") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def _save_users(self):
        """Save user database"""
        users_file = Path("config/users.json")
        users_file.parent.mkdir(exist_ok=True)
        try:
            with open(users_file, "w") as f:
                json.dump(self.users, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save users: {e}")

    def hash_password(self, password: str) -> str:
        """Hash a password securely"""
        salt = secrets.token_hex(16)
        hash_obj = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000
        )
        return f"{salt}${hash_obj.hex()}"

    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify a password against its hash"""
        try:
            salt, hash_hex = hashed.split("$")
            hash_obj = hashlib.pbkdf2_hmac(
                "sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000
            )
            return hash_obj.hex() == hash_hex
        except Exception:
            return False

    def create_user(
        self, username: str, password: str, email: str, role: str = "user"
    ) -> bool:
        """Create a new user"""
        if username in self.users:
            return False

        self.users[username] = {
            "email": email,
            "password_hash": self.hash_password(password),
            "role": role,
            "created_at": datetime.datetime.utcnow().isoformat(),
            "last_login": None,
            "is_active": True,
        }

        self._save_users()
        return True

    def authenticate_user(
        self, username: str, password: str
    ) -> Optional[Dict[str, Any]]:
        """Authenticate a user and return user info"""
        if username not in self.users:
            return None

        user = self.users[username]
        if not user.get("is_active", True):
            return None

        if not self.verify_password(password, user["password_hash"]):
            return None

        # Update last login
        user["last_login"] = datetime.datetime.utcnow().isoformat()
        self._save_users()

        return {
            "username": username,
            "email": user["email"],
            "role": user["role"],
            "created_at": user["created_at"],
        }

    def generate_token(
        self, user_info: Dict[str, Any], token_type: str = "access"
    ) -> str:
        """Generate a JWT token"""
        now = datetime.datetime.utcnow()

        if token_type == "access":
            expiration = now + datetime.timedelta(hours=self.expiration_hours)
        else:  # refresh token
            expiration = now + datetime.timedelta(days=self.refresh_expiration_days)

        payload = {
            "sub": user_info["username"],
            "email": user_info["email"],
            "role": user_info["role"],
            "type": token_type,
            "iat": now,
            "exp": expiration,
        }

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode a JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def refresh_token(self, refresh_token: str) -> Optional[str]:
        """Generate a new access token using a refresh token"""
        payload = self.verify_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            return None

        # Get user info
        username = payload["sub"]
        if username not in self.users:
            return None

        user_info = {
            "username": username,
            "email": payload["email"],
            "role": payload["role"],
        }

        return self.generate_token(user_info, "access")

    def login(self, username: str, password: str) -> Optional[Dict[str, str]]:
        """Login a user and return tokens"""
        user_info = self.authenticate_user(username, password)
        if not user_info:
            return None

        return {
            "access_token": self.generate_token(user_info, "access"),
            "refresh_token": self.generate_token(user_info, "refresh"),
            "user_info": user_info,
        }

    def get_user_info(self, token: str) -> Optional[Dict[str, Any]]:
        """Get user information from token"""
        payload = self.verify_token(token)
        if not payload:
            return None

        username = payload["sub"]
        if username not in self.users:
            return None

        return {
            "username": username,
            "email": payload["email"],
            "role": payload["role"],
        }

    def has_permission(self, token: str, permission: str) -> bool:
        """Check if user has specific permission"""
        user_info = self.get_user_info(token)
        if not user_info:
            return False

        # Simple role-based permissions
        role_permissions = {
            "admin": ["read", "write", "delete", "admin"],
            "user": ["read", "write"],
            "viewer": ["read"],
        }

        user_role = user_info["role"]
        return permission in role_permissions.get(user_role, [])

    def create_default_admin(self):
        """Create a default admin user if no users exist"""
        if not self.users:
            self.create_user(
                username="admin",
                password="admin123",  # Should be changed in production
                email="admin@autodevcore.com",
                role="admin",
            )
            print("✅ Default admin user created: admin/admin123")
            print("⚠️  Please change the default password in production!")


# Global instance
jwt_auth = JWTAuthManager()
