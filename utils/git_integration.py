#!/usr/bin/env python3
"""
AutoDevCore Git Integration - BULLETPROOF EDITION
Comprehensive Git integration for generated projects with automatic repo management
"""

import json
import logging
import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

class GitIntegration:
    """Bulletproof Git integration for AutoDevCore projects."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.git_config = {
            "user.name": "AutoDevCore",
            "user.email": "autodevcore@example.com",
            "init.defaultBranch": "main",
            "pull.rebase": "false",
            "push.autoSetupRemote": "true",
        }

    def initialize_repository(
        self, project_path: Path, project_name: str, description: str = ""
    ) -> Dict[str, Any]:
        """Initialize a new Git repository with bulletproof configuration."""
        try:
            # Ensure project directory exists
            project_path.mkdir(parents=True, exist_ok=True)

            # Change to project directory
            original_cwd = os.getcwd()
            os.chdir(project_path)

            # Initialize Git repository
            self._run_git_command(["init"])

            # Configure Git
            for key, value in self.git_config.items():
                self._run_git_command(["config", key, value])

            # Create comprehensive .gitignore
            self._create_gitignore(project_path)

            # Create initial commit with project structure
            self._create_initial_commit(project_name, description)

            # Create development branch
            self._run_git_command(["checkout", "-b", "develop"])

            # Return to original directory
            os.chdir(original_cwd)

            return {
                "success": True,
                "repository_path": str(project_path),
                "main_branch": "main",
                "develop_branch": "develop",
                "message": f"Git repository initialized successfully for {project_name}",
            }

        except Exception as e:
            self.logger.error(f"Failed to initialize Git repository: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to initialize Git repository",
            }

    def commit_generated_code(
        self, project_path: Path, commit_message: str = None, files: List[str] = None
    ) -> Dict[str, Any]:
        """Commit generated code with intelligent commit messages."""
        try:
            original_cwd = os.getcwd()
            os.chdir(project_path)

            # Generate intelligent commit message if not provided
            if not commit_message:
                commit_message = self._generate_commit_message(project_path)

            # Add files to staging
            if files:
                for file_path in files:
                    if Path(file_path).exists():
                        self._run_git_command(["add", file_path])
            else:
                # Add all files except those in .gitignore
                self._run_git_command(["add", "."])

            # Check if there are changes to commit
            status = self._run_git_command(["status", "--porcelain"])
            if not status.strip():
                return {
                    "success": True,
                    "message": "No changes to commit",
                    "commit_hash": None,
                }

            # Commit changes
            self._run_git_command(["commit", "-m", commit_message])

            # Get commit hash
            commit_hash = self._run_git_command(["rev-parse", "HEAD"]).strip()

            os.chdir(original_cwd)

            return {
                "success": True,
                "commit_hash": commit_hash,
                "commit_message": commit_message,
                "message": "Code committed successfully",
            }

        except Exception as e:
            self.logger.error(f"Failed to commit code: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to commit code",
            }

    def create_feature_branch(
        self, project_path: Path, feature_name: str
    ) -> Dict[str, Any]:
        """Create a feature branch for development."""
        try:
            original_cwd = os.getcwd()
            os.chdir(project_path)

            # Ensure we're on develop branch
            self._run_git_command(["checkout", "develop"])
            self._run_git_command(["pull", "origin", "develop"])

            # Create feature branch
            branch_name = f"feature/{feature_name.lower().replace(' ', '-')}"
            self._run_git_command(["checkout", "-b", branch_name])

            os.chdir(original_cwd)

            return {
                "success": True,
                "branch_name": branch_name,
                "message": f"Feature branch '{branch_name}' created successfully",
            }

        except Exception as e:
            self.logger.error(f"Failed to create feature branch: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to create feature branch",
            }

    def setup_remote_repository(
        self, project_path: Path, remote_url: str, remote_name: str = "origin"
    ) -> Dict[str, Any]:
        """Setup remote repository connection."""
        try:
            original_cwd = os.getcwd()
            os.chdir(project_path)

            # Add remote
            self._run_git_command(["remote", "add", remote_name, remote_url])

            # Push to remote
            self._run_git_command(["push", "-u", remote_name, "main"])
            self._run_git_command(["push", "-u", remote_name, "develop"])

            os.chdir(original_cwd)

            return {
                "success": True,
                "remote_url": remote_url,
                "remote_name": remote_name,
                "message": f"Remote repository '{remote_name}' configured successfully",
            }

        except Exception as e:
            self.logger.error(f"Failed to setup remote repository: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to setup remote repository",
            }

    def create_release_tag(
        self, project_path: Path, version: str, message: str = None
    ) -> Dict[str, Any]:
        """Create a release tag for version management."""
        try:
            original_cwd = os.getcwd()
            os.chdir(project_path)

            # Ensure we're on main branch
            self._run_git_command(["checkout", "main"])
            self._run_git_command(["pull", "origin", "main"])

            # Create tag
            tag_message = message or f"Release version {version}"
            self._run_git_command(["tag", "-a", f"v{version}", "-m", tag_message])

            # Push tag to remote
            self._run_git_command(["push", "origin", f"v{version}"])

            os.chdir(original_cwd)

            return {
                "success": True,
                "version": version,
                "tag_name": f"v{version}",
                "message": f"Release tag v{version} created successfully",
            }

        except Exception as e:
            self.logger.error(f"Failed to create release tag: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to create release tag",
            }

    def get_repository_status(self, project_path: Path) -> Dict[str, Any]:
        """Get comprehensive repository status."""
        try:
            original_cwd = os.getcwd()
            os.chdir(project_path)

            # Get current branch
            current_branch = self._run_git_command(["branch", "--show-current"]).strip()

            # Get commit history
            commits = (
                self._run_git_command(["log", "--oneline", "-10"]).strip().split("\n")
            )

            # Get status
            status = self._run_git_command(["status", "--porcelain"]).strip()

            # Get remote info
            remotes = self._run_git_command(["remote", "-v"]).strip()

            # Get last commit info
            last_commit = self._run_git_command(
                ["log", "-1", "--pretty=format:%H|%an|%ae|%ad|%s"]
            ).strip()

            os.chdir(original_cwd)

            return {
                "success": True,
                "current_branch": current_branch,
                "commit_count": len(commits),
                "recent_commits": commits,
                "has_changes": bool(status),
                "remotes": remotes,
                "last_commit": last_commit,
                "repository_path": str(project_path),
            }

        except Exception as e:
            self.logger.error(f"Failed to get repository status: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to get repository status",
            }

    def _create_gitignore(self, project_path: Path) -> None:
        """Create comprehensive .gitignore file."""
        gitignore_content = """# AutoDevCore Generated .gitignore

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Logs
*.log
logs/
log/

# Database
*.db
*.sqlite
*.sqlite3

# Environment variables
.env
.env.local
.env.development
.env.test
.env.production

# Secrets
secrets.json
*.key
*.pem
*.p12
*.pfx

# Temporary files
*.tmp
*.temp
.cache/

# Large files
*.zip
*.tar.gz
*.rar
*.7z

# AI Models (if large)
models/
*.gguf
*.bin

# Node.js (if applicable)
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# React (if applicable)
build/
static/

# Docker
.dockerignore

# Kubernetes
*.yaml
*.yml
!docker-compose.yml

# Testing
.coverage
.pytest_cache/
htmlcov/
.tox/

# Documentation
docs/_build/
site/

# AutoDevCore specific
thought_trail.json
architecture.md
evaluation_reports/
test_outputs/
"""

        gitignore_path = project_path / ".gitignore"
        with open(gitignore_path, "w") as f:
            f.write(gitignore_content)

    def _create_initial_commit(self, project_name: str, description: str) -> None:
        """Create initial commit with project structure."""
        # Add all files
        self._run_git_command(["add", "."])

        # Create initial commit message
        commit_message = f"""🎉 Initial commit: {project_name}

{description}

Generated by AutoDevCore - The core of intelligent development.

Features:
- Complete project structure
- Comprehensive documentation
- Security configurations
- Performance optimizations
- Testing framework
- Deployment configurations

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

        self._run_git_command(["commit", "-m", commit_message])

    def _generate_commit_message(self, project_path: Path) -> str:
        """Generate intelligent commit message based on changes."""
        try:
            # Get list of changed files
            status = self._run_git_command(["status", "--porcelain"]).strip()

            if not status:
                return "No changes detected"

            # Analyze changes
            files = [line.split()[-1] for line in status.split("\n") if line.strip()]

            # Categorize changes
            categories = {
                "features": [],
                "security": [],
                "docs": [],
                "tests": [],
                "config": [],
                "other": [],
            }

            for file_path in files:
                if any(
                    keyword in file_path.lower()
                    for keyword in ["security", "auth", "encrypt"]
                ):
                    categories["security"].append(file_path)
                elif any(keyword in file_path.lower() for keyword in ["test", "spec"]):
                    categories["tests"].append(file_path)
                elif any(
                    keyword in file_path.lower() for keyword in ["readme", "doc", "md"]
                ):
                    categories["docs"].append(file_path)
                elif any(
                    keyword in file_path.lower()
                    for keyword in ["config", "settings", "env"]
                ):
                    categories["config"].append(file_path)
                elif any(
                    keyword in file_path.lower()
                    for keyword in ["feature", "api", "model", "view"]
                ):
                    categories["features"].append(file_path)
                else:
                    categories["other"].append(file_path)

            # Generate commit message
            message_parts = []

            if categories["features"]:
                message_parts.append("✨ Add new features")
            if categories["security"]:
                message_parts.append("🔒 Enhance security")
            if categories["tests"]:
                message_parts.append("🧪 Add tests")
            if categories["docs"]:
                message_parts.append("📚 Update documentation")
            if categories["config"]:
                message_parts.append("⚙️ Update configuration")
            if categories["other"]:
                message_parts.append("🔧 General improvements")

            if not message_parts:
                message_parts.append("🔧 Update project files")

            commit_message = " | ".join(message_parts)
            commit_message += f"\n\nUpdated {len(files)} files"

            return commit_message

        except Exception as e:
            self.logger.warning(f"Failed to generate commit message: {e}")
            return f"🔧 Update project files - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    def _run_git_command(self, args: List[str]) -> str:
        """Run Git command with error handling."""
        try:
            result = subprocess.run(
                ["git"] + args, capture_output=True, text=True, check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Git command failed: {' '.join(['git'] + args)}")
            self.logger.error(f"Error: {e.stderr}")
            raise e

    def create_project_with_git(
        self,
        project_name: str,
        project_path: Path,
        description: str = "",
        remote_url: str = None,
    ) -> Dict[str, Any]:
        """Complete project setup with Git integration."""
        try:
            # Initialize repository
            init_result = self.initialize_repository(
                project_path, project_name, description
            )
            if not init_result["success"]:
                return init_result

            # Setup remote if provided
            if remote_url:
                remote_result = self.setup_remote_repository(project_path, remote_url)
                if not remote_result["success"]:
                    return remote_result

            # Get repository status
            status_result = self.get_repository_status(project_path)

            return {
                "success": True,
                "project_name": project_name,
                "project_path": str(project_path),
                "git_initialized": init_result["success"],
                "remote_configured": bool(remote_url),
                "repository_status": status_result,
                "message": f"Project '{project_name}' created with Git integration",
            }

        except Exception as e:
            self.logger.error(f"Failed to create project with Git: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to create project with Git integration",
            }

# Global instance for easy access
git_integration = GitIntegration()
