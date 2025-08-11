#!/usr/bin/env python3
"""
AutoDevCore CORS Configuration System
Provides Cross-Origin Resource Sharing configuration for web components
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import re


@dataclass
class CORSConfig:
    """CORS Configuration settings"""

    allowed_origins: List[str]
    allowed_methods: List[str]
    allowed_headers: List[str]
    allow_credentials: bool
    max_age: int
    expose_headers: List[str]


class CORSMiddleware:
    """CORS Middleware for handling cross-origin requests"""

    def __init__(self, config: CORSConfig):
        self.config = config

    def add_cors_headers(self, response_headers: Dict[str, str], origin: str = None):
        """Add CORS headers to response"""
        if origin and origin in self.config.allowed_origins:
            response_headers["Access-Control-Allow-Origin"] = origin
        elif "*" in self.config.allowed_origins:
            response_headers["Access-Control-Allow-Origin"] = "*"

        response_headers["Access-Control-Allow-Methods"] = ", ".join(
            self.config.allowed_methods
        )
        response_headers["Access-Control-Allow-Headers"] = ", ".join(
            self.config.allowed_headers
        )
        response_headers["Access-Control-Max-Age"] = str(self.config.max_age)

        if self.config.expose_headers:
            response_headers["Access-Control-Expose-Headers"] = ", ".join(
                self.config.expose_headers
            )

        if self.config.allow_credentials:
            response_headers["Access-Control-Allow-Credentials"] = "true"

    def handle_preflight(
        self, request_method: str, request_headers: List[str]
    ) -> Dict[str, Any]:
        """Handle CORS preflight requests"""
        # Check if request method is allowed
        if request_method not in self.config.allowed_methods:
            return {"status": 405, "headers": {}, "body": "Method Not Allowed"}

        # Check if all request headers are allowed
        for header in request_headers:
            if header.lower() not in [h.lower() for h in self.config.allowed_headers]:
                return {"status": 400, "headers": {}, "body": "Header Not Allowed"}

        # Return successful preflight response
        headers = {}
        self.add_cors_headers(headers)

        return {"status": 200, "headers": headers, "body": ""}


class CORSManager:
    """CORS Configuration Manager for AutoDevCore"""

    def __init__(self, config_file: str = "config/cors_config.json"):
        self.config_file = Path(config_file)
        self.config_file.parent.mkdir(exist_ok=True)
        self.config = self._load_config()
        self.middleware = CORSMiddleware(self.config)

    def _load_config(self) -> CORSConfig:
        """Load CORS configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, "r") as f:
                    data = json.load(f)
                    return CORSConfig(
                        allowed_origins=data.get("allowed_origins", ["*"]),
                        allowed_methods=data.get(
                            "allowed_methods",
                            ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                        ),
                        allowed_headers=data.get("allowed_headers", ["*"]),
                        allow_credentials=data.get("allow_credentials", False),
                        max_age=data.get("max_age", 3600),
                        expose_headers=data.get("expose_headers", []),
                    )
            except Exception as e:
                print(f"Warning: Could not load CORS config: {e}")

        # Return default configuration
        return CORSConfig(
            allowed_origins=["*"],
            allowed_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            allowed_headers=["*"],
            allow_credentials=False,
            max_age=3600,
            expose_headers=[],
        )

    def save_config(self):
        """Save CORS configuration to file"""
        try:
            config_data = {
                "allowed_origins": self.config.allowed_origins,
                "allowed_methods": self.config.allowed_methods,
                "allowed_headers": self.config.allowed_headers,
                "allow_credentials": self.config.allow_credentials,
                "max_age": self.config.max_age,
                "expose_headers": self.config.expose_headers,
            }

            with open(self.config_file, "w") as f:
                json.dump(config_data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save CORS config: {e}")

    def update_config(self, **kwargs):
        """Update CORS configuration"""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)

        self.save_config()
        self.middleware = CORSMiddleware(self.config)

    def add_allowed_origin(self, origin: str):
        """Add an allowed origin"""
        if origin not in self.config.allowed_origins:
            self.config.allowed_origins.append(origin)
            self.save_config()
            self.middleware = CORSMiddleware(self.config)

    def remove_allowed_origin(self, origin: str):
        """Remove an allowed origin"""
        if origin in self.config.allowed_origins:
            self.config.allowed_origins.remove(origin)
            self.save_config()
            self.middleware = CORSMiddleware(self.config)

    def is_origin_allowed(self, origin: str) -> bool:
        """Check if an origin is allowed"""
        return (
            origin in self.config.allowed_origins or "*" in self.config.allowed_origins
        )

    def validate_origin(self, origin: str) -> bool:
        """Validate origin format"""
        # Basic origin validation
        if origin == "*":
            return True

        # Check for valid URL format
        pattern = r"^https?://[a-zA-Z0-9.-]+(:\d+)?$"
        return bool(re.match(pattern, origin))

    def get_security_headers(self) -> Dict[str, str]:
        """Get security headers for CORS"""
        headers = {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Referrer-Policy": "strict-origin-when-cross-origin",
        }

        # Add CORS headers
        self.middleware.add_cors_headers(headers)

        return headers

    def create_secure_config(self) -> CORSConfig:
        """Create a secure CORS configuration"""
        return CORSConfig(
            allowed_origins=[
                "http://localhost:3000",
                "http://localhost:8501",
            ],  # Specific origins
            allowed_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            allowed_headers=["Content-Type", "Authorization", "X-Requested-With"],
            allow_credentials=True,
            max_age=3600,
            expose_headers=["X-Total-Count", "X-Page-Count"],
        )

    def create_development_config(self) -> CORSConfig:
        """Create a development CORS configuration"""
        return CORSConfig(
            allowed_origins=["*"],  # Allow all origins in development
            allowed_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            allowed_headers=["*"],
            allow_credentials=False,
            max_age=3600,
            expose_headers=[],
        )

    def get_config_summary(self) -> Dict[str, Any]:
        """Get a summary of the current CORS configuration"""
        return {
            "allowed_origins_count": len(self.config.allowed_origins),
            "allowed_methods": self.config.allowed_methods,
            "allowed_headers_count": len(self.config.allowed_headers),
            "allow_credentials": self.config.allow_credentials,
            "max_age": self.config.max_age,
            "expose_headers_count": len(self.config.expose_headers),
            "is_secure": not (
                "*" in self.config.allowed_origins and self.config.allow_credentials
            ),
        }


# Global instance
cors_manager = CORSManager()
