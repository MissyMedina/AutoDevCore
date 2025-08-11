"""
Validation Utilities
"""

import re
from typing import Any, Dict, List
from fastapi import HTTPException, status


def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def validate_password_strength(password: str) -> Dict[str, Any]:
    """Validate password strength."""
    errors = []

    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")

    if not re.search(r"[A-Z]", password):
        errors.append("Password must contain at least one uppercase letter")

    if not re.search(r"[a-z]", password):
        errors.append("Password must contain at least one lowercase letter")

    if not re.search(r"\d", password):
        errors.append("Password must contain at least one number")

    return {"is_valid": len(errors) == 0, "errors": errors}


def sanitize_input(input_str: str) -> str:
    """Basic input sanitization."""
    # Remove potentially dangerous characters
    dangerous_chars = ["<", ">", '"', "'", "&"]
    for char in dangerous_chars:
        input_str = input_str.replace(char, "")
    return input_str.strip()


def validate_request_size(content_length: int, max_size: int = 1024 * 1024) -> bool:
    """Validate request size."""
    return content_length <= max_size
