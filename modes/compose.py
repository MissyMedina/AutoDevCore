"""
Compose Mode for AutoDevCore

This mode orchestrates the complete application generation process.
"""

import os
from pathlib import Path

from agents.code_generator import CodeGeneratorAgent
from agents.composer import ComposerAgent
from agents.prd_writer import PRDWriterAgent
from agents.readme_writer import READMEWriterAgent

from .base import BaseMode


class ComposeMode(BaseMode):
    """Mode for composing complete applications from ideas."""

    def __init__(self, idea: str, output_dir: str, verbose: bool = False):
        super().__init__(output_dir, verbose)
        self.idea = idea
        self.composer = ComposerAgent()
        self.prd_writer = PRDWriterAgent()
        self.code_generator = CodeGeneratorAgent()
        self.readme_writer = READMEWriterAgent()

    def execute(self):
        """Execute the compose mode to generate a complete application."""
        print(f"🚀 Starting AutoDevCore Compose Mode")
        print(f"💡 Idea: {self.idea}")
        print(f"📁 Output Directory: {self.output_dir}")
        print()

        # Step 1: Analyze idea and create app plan
        self.log_thought("Composer", "Starting app idea analysis", {"idea": self.idea})
        app_plan = self.composer.create_app_plan(self.idea)
        self.log_thought("Composer", "App plan created", {"plan": app_plan})

        # Step 2: Generate PRD
        self.log_thought("PRD Writer", "Starting PRD generation")
        prd_content = self.prd_writer.generate_prd(self.idea, app_plan)
        self.log_thought("PRD Writer", "PRD generated successfully")

        # Step 3: Generate codebase
        self.log_thought("Code Generator", "Starting code generation")
        app_name = app_plan.get("app_name", "AutoDevApp")
        app_dir = self.output_dir / app_name
        app_dir.mkdir(exist_ok=True)

        code_files = self.code_generator.generate_codebase(app_plan, app_dir)
        self.log_thought(
            "Code Generator", "Codebase generated", {"files": list(code_files.keys())}
        )

        # Step 4: Generate README
        self.log_thought("README Writer", "Starting README generation")
        readme_content = self.readme_writer.generate_readme(app_plan, app_name)
        self.log_thought("README Writer", "README generated successfully")

        # Step 5: Save all files
        self._save_files(app_plan, prd_content, code_files, readme_content, app_name)

        # Step 6: Generate thought trail and diagrams
        self.save_thought_trail()
        self.generate_mermaid_diagram()

        print(f"\n🎉 Application generation complete!")
        print(f"📁 Application saved to: {app_dir}")
        print(f"📄 PRD saved to: {self.output_dir / 'PRD.md'}")
        print(f"📄 README saved to: {app_dir / 'README.md'}")
        print(f"🧠 Thought trail saved to: {self.output_dir / 'thought_trail.json'}")
        print(
            f"📊 Architecture diagram saved to: {self.output_dir / 'architecture.md'}"
        )

    def _save_files(
        self,
        app_plan: dict,
        prd_content: str,
        code_files: dict,
        readme_content: str,
        app_name: str,
    ):
        """Save all generated files."""
        # Save PRD
        prd_file = self.output_dir / "PRD.md"
        with open(prd_file, "w") as f:
            f.write(prd_content)

        # Save code files
        app_dir = self.output_dir / app_name
        for file_path, content in code_files.items():
            full_path = app_dir / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            with open(full_path, "w") as f:
                f.write(content)

        # Save README
        readme_file = app_dir / "README.md"
        with open(readme_file, "w") as f:
            f.write(readme_content)

        # Save app plan as JSON
        plan_file = self.output_dir / "app_plan.json"

        import json

        with open(plan_file, "w") as f:
            json.dump(app_plan, f, indent=2)

    def _generate_dependency_files(self, app_dir: Path, app_plan: dict):
        """Generate dependency files based on the tech stack."""
        tech_stack = app_plan.get("tech_stack", {})
        backend = tech_stack.get("backend", "python")

        if "python" in backend.lower():
            requirements_file = app_dir / "requirements.txt"
            requirements_content = """fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
sqlalchemy==2.0.23
python-dotenv==1.0.0
python-multipart==0.0.6
passlib[bcrypt]==1.7.4
python-jose[cryptography]==3.3.0
"""
            with open(requirements_file, "w") as f:
                f.write(requirements_content)

        elif "node" in backend.lower():
            package_file = app_dir / "package.json"
            package_content = """{
  "name": "autodev-app",
  "version": "1.0.0",
  "description": "AutoDevCore generated application",
  "main": "server.js",
  "scripts": {
    "start": "node server.js",
    "dev": "nodemon server.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "cors": "^2.8.5",
    "helmet": "^7.1.0",
    "dotenv": "^16.3.1"
  },
  "devDependencies": {
    "nodemon": "^3.0.2"
  }
}"""
            with open(package_file, "w") as f:
                f.write(package_content)
