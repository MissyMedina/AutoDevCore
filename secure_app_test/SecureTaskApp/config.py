"""
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
