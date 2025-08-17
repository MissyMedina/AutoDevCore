"""
Authentication Dependencies
"""

from typing import Optional

from auth.auth import get_current_active_user
from database import get_db
from fastapi import Depends, HTTPException, status
from models import User
from sqlalchemy.orm import Session

def require_admin(current_user: User = Depends(get_current_active_user)) -> User:
    """Require admin role."""
    if not hasattr(current_user, "is_admin") or not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required"
        )
    return current_user

def require_user_permission(
    user_id: int, current_user: User = Depends(get_current_active_user)
) -> User:
    """Require user to access their own data or be admin."""
    if current_user.id != user_id and not getattr(current_user, "is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    return current_user
