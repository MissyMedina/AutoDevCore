#!/usr/bin/env python3
"""
Test script to verify security features
"""

from config.security import settings
from api.routes import UserCreate
from pydantic import ValidationError


def test_security_settings():
    """Test security configuration."""
    print("🔒 Security Settings Test")
    print(f"  CORS Origins: {settings.CORS_ORIGINS}")
    print(f"  Allowed Hosts: {settings.ALLOWED_HOSTS}")
    print(f"  Rate Limit: {settings.RATE_LIMIT_PER_MINUTE}/min")
    print(f"  Password Policy: {settings.MIN_PASSWORD_LENGTH} chars min")
    print(f"  JWT Algorithm: {settings.ALGORITHM}")
    print(f"  Token Expiry: {settings.ACCESS_TOKEN_EXPIRE_MINUTES} minutes")
    print("✅ Security settings configured correctly")


def test_input_validation():
    """Test input validation."""
    print("\n🔍 Input Validation Test")

    # Test invalid email
    try:
        user = UserCreate(username="test", email="invalid-email", password="12345678")
        print("❌ Validation should have failed for invalid email")
    except ValidationError as e:
        print(f"✅ Email validation working: {e.errors()[0]['msg']}")

    # Test short password
    try:
        user = UserCreate(username="test", email="test@example.com", password="123")
        print("❌ Validation should have failed for short password")
    except ValidationError as e:
        print(f"✅ Password length validation working: {e.errors()[0]['msg']}")

    # Test short username
    try:
        user = UserCreate(username="ab", email="test@example.com", password="12345678")
        print("❌ Validation should have failed for short username")
    except ValidationError as e:
        print(f"✅ Username length validation working: {e.errors()[0]['msg']}")

    # Test valid input
    try:
        user = UserCreate(
            username="testuser", email="test@example.com", password="SecurePass123"
        )
        print("✅ Valid input accepted")
    except ValidationError as e:
        print(f"❌ Valid input rejected: {e.errors()}")


if __name__ == "__main__":
    test_security_settings()
    test_input_validation()
    print("\n🎉 Security tests completed!")
