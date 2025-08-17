"""
Composer Agent for AutoDevCore

This agent analyzes app ideas and creates detailed development plans.
"""

import json
from pathlib import Path

from integrations import gpt_oss_client


class ComposerAgent:
    """Agent responsible for analyzing app ideas and creating development plans."""

    def __init__(self):
        self.name = "Composer"

    def create_app_plan(self, idea: str) -> dict:
        """
        Create a comprehensive development plan for an app idea.

        Args:
            idea: The app idea description

        Returns:
            Dict containing the app plan with features, tech stack, architecture, etc.
        """
        print(f"🤖 {self.name}: Analyzing app idea and creating development plan...")

        try:
            # Use GPT-OSS to generate the app plan
            plan = gpt_oss_client.generate_app_plan(idea)

            # Ensure we have a structured plan
            if isinstance(plan, dict) and "plan" not in plan:
                # If GPT-OSS returned a structured plan, use it
                structured_plan = plan
            else:
                # Fallback to our original template structure
                structured_plan = self._create_fallback_plan(
                    idea, plan.get("plan", str(plan))
                )

            print(f"✅ {self.name}: Development plan created successfully")
            return structured_plan

        except Exception as e:
            print(
                f"⚠️ {self.name}: Error generating plan with GPT-OSS, using fallback: {e}"
            )
            return self._create_fallback_plan(idea)

    def _create_fallback_plan(self, idea: str, gpt_plan: str = None) -> dict:
        """Create a fallback plan if GPT-OSS fails."""
        return {
            "app_name": self._generate_app_name(idea),
            "description": idea,
            "features": [
                "User authentication and authorization",
                "CRUD operations for core entities",
                "RESTful API endpoints",
                "Database integration",
                "Basic UI/UX",
                "Error handling and logging",
            ],
            "tech_stack": {
                "backend": "Python/FastAPI",
                "database": "SQLite (development) / PostgreSQL (production)",
                "frontend": "HTML/CSS/JavaScript",
                "deployment": "Docker",
            },
            "architecture": {
                "pattern": "MVC (Model-View-Controller)",
                "layers": ["API Layer", "Business Logic", "Data Access", "Database"],
            },
            "database_schema": {
                "users": {
                    "id": "INTEGER PRIMARY KEY",
                    "username": "VARCHAR(50) UNIQUE",
                    "email": "VARCHAR(100) UNIQUE",
                    "password_hash": "VARCHAR(255)",
                    "created_at": "TIMESTAMP",
                }
            },
            "api_endpoints": [
                "GET /api/health",
                "POST /api/auth/register",
                "POST /api/auth/login",
                "GET /api/users/me",
                "PUT /api/users/me",
            ],
            "ui_components": [
                "Login/Register forms",
                "Dashboard",
                "Navigation menu",
                "Data tables",
                "Forms for CRUD operations",
            ],
            "deployment": {
                "containerization": "Docker",
                "orchestration": "Docker Compose",
                "environment": "Development/Production configs",
            },
            "gpt_plan": gpt_plan,  # Include the GPT-OSS plan if available
        }

    def _generate_app_name(self, idea: str) -> str:
        """Generate an app name based on the idea."""
        try:
            # Try to use GPT-OSS for name generation
            prompt = f"Generate a catchy, professional app name for: {idea}. Return only the name, no explanation."
            response = gpt_oss_client.generate(prompt, temperature=0.8, max_tokens=50)
            name = response.get("message", {}).get("content", "").strip()

            # Clean up the name
            if name and len(name) < 50:
                return name.replace('"', "").replace("'", "").strip()
        except:
            pass

        # Fallback name generation
        words = idea.lower().split()
        if len(words) >= 2:
            return f"{words[0].capitalize()}{words[1].capitalize()}App"
        else:
            return f"{words[0].capitalize()}App" if words else "AutoDevApp"
