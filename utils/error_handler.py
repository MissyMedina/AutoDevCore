#!/usr/bin/env python3
"""
AutoDevCore Error Handler - BULLETPROOF EDITION
Comprehensive error handling with descriptive messages and actionable solutions
"""

import traceback
import sys
import logging
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from enum import Enum
from dataclasses import dataclass, field


class ErrorSeverity(Enum):
    """Error severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ErrorCategory(Enum):
    """Error categories for better organization."""
    AI_MODEL = "ai_model"
    NETWORK = "network"
    CONFIGURATION = "configuration"
    PERMISSION = "permission"
    VALIDATION = "validation"
    INTEGRATION = "integration"
    SYSTEM = "system"
    USER_INPUT = "user_input"
    SECURITY = "security"
    PERFORMANCE = "performance"


@dataclass
class ErrorContext:
    """Context information for error handling."""
    operation: str = ""
    component: str = ""
    user_input: str = ""
    system_info: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class ErrorSolution:
    """Solution information for errors."""
    description: str
    steps: List[str] = field(default_factory=list)
    code_example: str = ""
    documentation_url: str = ""
    command: str = ""


@dataclass
class ErrorInfo:
    """Comprehensive error information."""
    error_type: str
    message: str
    severity: ErrorSeverity
    category: ErrorCategory
    context: ErrorContext
    solution: Optional[ErrorSolution] = None
    original_exception: Optional[Exception] = None
    traceback: str = ""


class BulletproofErrorHandler:
    """Bulletproof error handling with comprehensive solutions."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.error_patterns = self._initialize_error_patterns()
        self.solutions_database = self._initialize_solutions_database()
    
    def _initialize_error_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Initialize error pattern recognition."""
        return {
            # AI Model Errors
            "openai_api_error": {
                "patterns": [
                    "openai.error.APIError",
                    "openai.error.RateLimitError",
                    "openai.error.AuthenticationError",
                    "openai.error.InvalidRequestError"
                ],
                "category": ErrorCategory.AI_MODEL,
                "severity": ErrorSeverity.ERROR
            },
            "anthropic_api_error": {
                "patterns": [
                    "anthropic.error.APIError",
                    "anthropic.error.RateLimitError",
                    "anthropic.error.AuthenticationError"
                ],
                "category": ErrorCategory.AI_MODEL,
                "severity": ErrorSeverity.ERROR
            },
            "gpt_oss_error": {
                "patterns": [
                    "requests.exceptions.ConnectionError",
                    "requests.exceptions.Timeout",
                    "Connection refused"
                ],
                "category": ErrorCategory.AI_MODEL,
                "severity": ErrorSeverity.WARNING
            },
            
            # Network Errors
            "network_timeout": {
                "patterns": [
                    "requests.exceptions.Timeout",
                    "timeout",
                    "timed out"
                ],
                "category": ErrorCategory.NETWORK,
                "severity": ErrorSeverity.WARNING
            },
            "connection_error": {
                "patterns": [
                    "requests.exceptions.ConnectionError",
                    "Connection refused",
                    "No route to host"
                ],
                "category": ErrorCategory.NETWORK,
                "severity": ErrorSeverity.ERROR
            },
            
            # Configuration Errors
            "missing_api_key": {
                "patterns": [
                    "OPENAI_API_KEY",
                    "ANTHROPIC_API_KEY",
                    "API key not found",
                    "No API key"
                ],
                "category": ErrorCategory.CONFIGURATION,
                "severity": ErrorSeverity.ERROR
            },
            "invalid_config": {
                "patterns": [
                    "Invalid configuration",
                    "Config error",
                    "Settings error"
                ],
                "category": ErrorCategory.CONFIGURATION,
                "severity": ErrorSeverity.ERROR
            },
            
            # Permission Errors
            "permission_denied": {
                "patterns": [
                    "Permission denied",
                    "Access denied",
                    "Forbidden"
                ],
                "category": ErrorCategory.PERMISSION,
                "severity": ErrorSeverity.ERROR
            },
            
            # Validation Errors
            "validation_error": {
                "patterns": [
                    "ValidationError",
                    "Invalid input",
                    "Invalid format"
                ],
                "category": ErrorCategory.VALIDATION,
                "severity": ErrorSeverity.WARNING
            },
            
            # Integration Errors
            "git_error": {
                "patterns": [
                    "git error",
                    "Git command failed",
                    "Repository error"
                ],
                "category": ErrorCategory.INTEGRATION,
                "severity": ErrorSeverity.ERROR
            },
            
            # System Errors
            "file_not_found": {
                "patterns": [
                    "FileNotFoundError",
                    "No such file or directory"
                ],
                "category": ErrorCategory.SYSTEM,
                "severity": ErrorSeverity.ERROR
            },
            "memory_error": {
                "patterns": [
                    "MemoryError",
                    "Out of memory"
                ],
                "category": ErrorCategory.SYSTEM,
                "severity": ErrorSeverity.CRITICAL
            }
        }
    
    def _initialize_solutions_database(self) -> Dict[str, ErrorSolution]:
        """Initialize solutions database."""
        return {
            "openai_api_error": ErrorSolution(
                description="OpenAI API error occurred. This is usually due to API key issues, rate limits, or invalid requests.",
                steps=[
                    "Check if your OpenAI API key is valid and properly configured",
                    "Verify your API key has sufficient credits",
                    "Check if you've exceeded rate limits",
                    "Ensure your request format is correct",
                    "Try using a different AI model if available"
                ],
                code_example="""
# Example: Proper OpenAI configuration
import os
os.environ["OPENAI_API_KEY"] = "your-api-key-here"

# Check API key
if not os.getenv("OPENAI_API_KEY"):
    print("❌ OpenAI API key not found")
    print("💡 Set your API key: export OPENAI_API_KEY='your-key'")
""",
                documentation_url="https://platform.openai.com/docs/api-reference/authentication",
                command="export OPENAI_API_KEY='your-api-key-here'"
            ),
            
            "anthropic_api_error": ErrorSolution(
                description="Anthropic API error occurred. Check your API key and request format.",
                steps=[
                    "Verify your Anthropic API key is correct",
                    "Check your account has sufficient credits",
                    "Ensure you're using the correct API endpoint",
                    "Verify your request format matches the API specification"
                ],
                code_example="""
# Example: Proper Anthropic configuration
import os
os.environ["ANTHROPIC_API_KEY"] = "your-api-key-here"

# Check API key
if not os.getenv("ANTHROPIC_API_KEY"):
    print("❌ Anthropic API key not found")
    print("💡 Set your API key: export ANTHROPIC_API_KEY='your-key'")
""",
                documentation_url="https://docs.anthropic.com/claude/reference/getting-started-with-the-api",
                command="export ANTHROPIC_API_KEY='your-api-key-here'"
            ),
            
            "gpt_oss_error": ErrorSolution(
                description="GPT-OSS (local Ollama) connection error. Ollama service may not be running.",
                steps=[
                    "Ensure Ollama is installed and running",
                    "Check if the GPT-OSS model is downloaded",
                    "Verify Ollama is accessible on localhost:11434",
                    "Try restarting the Ollama service"
                ],
                code_example="""
# Example: Start Ollama and download model
# 1. Start Ollama service
ollama serve

# 2. Download GPT-OSS model
ollama pull gpt-oss:20b

# 3. Test connection
curl http://localhost:11434/api/tags
""",
                documentation_url="https://ollama.ai/library/gpt-oss",
                command="ollama serve && ollama pull gpt-oss:20b"
            ),
            
            "network_timeout": ErrorSolution(
                description="Network timeout occurred. This may be due to slow internet or server issues.",
                steps=[
                    "Check your internet connection",
                    "Try again in a few moments",
                    "Use a different AI provider if available",
                    "Check if the service is experiencing downtime"
                ],
                code_example="""
# Example: Increase timeout
import requests
response = requests.get(url, timeout=60)  # 60 second timeout

# Or use local models for reliability
# ollama run gpt-oss:20b
""",
                documentation_url="",
                command=""
            ),
            
            "missing_api_key": ErrorSolution(
                description="API key is missing or not properly configured.",
                steps=[
                    "Set your API key as an environment variable",
                    "Check your .env file configuration",
                    "Verify the API key is correct",
                    "Ensure the API key has proper permissions"
                ],
                code_example="""
# Example: Set API keys
export OPENAI_API_KEY="your-openai-key"
export ANTHROPIC_API_KEY="your-anthropic-key"

# Or create .env file
echo "OPENAI_API_KEY=your-key" > .env
echo "ANTHROPIC_API_KEY=your-key" >> .env
""",
                documentation_url="",
                command="export OPENAI_API_KEY='your-key' && export ANTHROPIC_API_KEY='your-key'"
            ),
            
            "git_error": ErrorSolution(
                description="Git operation failed. Check your Git configuration and permissions.",
                steps=[
                    "Ensure Git is installed and configured",
                    "Check if you have write permissions to the directory",
                    "Verify your Git user configuration",
                    "Check if the repository is properly initialized"
                ],
                code_example="""
# Example: Configure Git
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Initialize repository
git init
git add .
git commit -m "Initial commit"
""",
                documentation_url="https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup",
                command="git config --global user.name 'Your Name' && git config --global user.email 'your.email@example.com'"
            ),
            
            "validation_error": ErrorSolution(
                description="Input validation failed. Check your input format and requirements.",
                steps=[
                    "Review the error message for specific validation issues",
                    "Check input format requirements",
                    "Ensure all required fields are provided",
                    "Verify data types and constraints"
                ],
                code_example="""
# Example: Proper input validation
def validate_input(data):
    if not data.get('name'):
        raise ValueError("Name is required")
    if len(data.get('description', '')) < 10:
        raise ValueError("Description must be at least 10 characters")
    return True
""",
                documentation_url="",
                command=""
            ),
            
            "file_not_found": ErrorSolution(
                description="File or directory not found. Check file paths and permissions.",
                steps=[
                    "Verify the file path is correct",
                    "Check if the file exists",
                    "Ensure you have read permissions",
                    "Create the directory if it doesn't exist"
                ],
                code_example="""
# Example: Safe file operations
import os
from pathlib import Path

# Create directory if it doesn't exist
Path("output").mkdir(exist_ok=True)

# Check if file exists before reading
if os.path.exists("config.json"):
    with open("config.json", "r") as f:
        config = json.load(f)
else:
    print("❌ config.json not found")
""",
                documentation_url="",
                command="mkdir -p output && ls -la"
            )
        }
    
    def handle_error(self, exception: Exception, context: ErrorContext = None) -> ErrorInfo:
        """Handle an exception and return comprehensive error information."""
        if context is None:
            context = ErrorContext()
        
        # Get error details
        error_type = type(exception).__name__
        error_message = str(exception)
        traceback_str = traceback.format_exc()
        
        # Analyze error pattern
        pattern_info = self._analyze_error_pattern(error_type, error_message, traceback_str)
        
        # Get solution
        solution = self._get_solution(pattern_info.get("pattern_key", ""))
        
        # Create error info
        error_info = ErrorInfo(
            error_type=error_type,
            message=error_message,
            severity=pattern_info.get("severity", ErrorSeverity.ERROR),
            category=pattern_info.get("category", ErrorCategory.SYSTEM),
            context=context,
            solution=solution,
            original_exception=exception,
            traceback=traceback_str
        )
        
        # Log error
        self._log_error(error_info)
        
        return error_info
    
    def _analyze_error_pattern(self, error_type: str, error_message: str, traceback_str: str) -> Dict[str, Any]:
        """Analyze error to determine pattern and category."""
        full_error_text = f"{error_type}: {error_message}\n{traceback_str}".lower()
        
        for pattern_key, pattern_info in self.error_patterns.items():
            for pattern in pattern_info["patterns"]:
                if pattern.lower() in full_error_text:
                    return {
                        "pattern_key": pattern_key,
                        "severity": pattern_info["severity"],
                        "category": pattern_info["category"]
                    }
        
        # Default pattern
        return {
            "pattern_key": "unknown_error",
            "severity": ErrorSeverity.ERROR,
            "category": ErrorCategory.SYSTEM
        }
    
    def _get_solution(self, pattern_key: str) -> Optional[ErrorSolution]:
        """Get solution for error pattern."""
        return self.solutions_database.get(pattern_key)
    
    def _log_error(self, error_info: ErrorInfo) -> None:
        """Log error with appropriate level."""
        log_message = f"""
🚨 ERROR: {error_info.error_type}
📝 Message: {error_info.message}
🏷️ Category: {error_info.category.value}
⚠️ Severity: {error_info.severity.value}
🔧 Operation: {error_info.context.operation}
📦 Component: {error_info.context.component}
⏰ Timestamp: {error_info.context.timestamp}
"""
        
        if error_info.solution:
            log_message += f"""
💡 Solution: {error_info.solution.description}
📋 Steps: {', '.join(error_info.solution.steps)}
"""
        
        if error_info.severity == ErrorSeverity.CRITICAL:
            self.logger.critical(log_message)
        elif error_info.severity == ErrorSeverity.ERROR:
            self.logger.error(log_message)
        elif error_info.severity == ErrorSeverity.WARNING:
            self.logger.warning(log_message)
        else:
            self.logger.info(log_message)
    
    def format_error_message(self, error_info: ErrorInfo) -> str:
        """Format error message for user display."""
        message = f"""
❌ {error_info.error_type.upper()}: {error_info.message}

🔧 Operation: {error_info.context.operation}
📦 Component: {error_info.context.component}
🏷️ Category: {error_info.category.value}
⚠️ Severity: {error_info.severity.value}
"""
        
        if error_info.solution:
            message += f"""
💡 SOLUTION:
{error_info.solution.description}

📋 STEPS TO RESOLVE:
"""
            for i, step in enumerate(error_info.solution.steps, 1):
                message += f"{i}. {step}\n"
            
            if error_info.solution.code_example:
                message += f"""
💻 CODE EXAMPLE:
{error_info.solution.code_example}
"""
            
            if error_info.solution.command:
                message += f"""
🚀 COMMAND TO RUN:
{error_info.solution.command}
"""
            
            if error_info.solution.documentation_url:
                message += f"""
📚 DOCUMENTATION:
{error_info.solution.documentation_url}
"""
        
        message += f"""
⏰ Timestamp: {error_info.context.timestamp}
🆔 Error ID: {id(error_info)}
"""
        
        return message
    
    def get_error_summary(self, error_info: ErrorInfo) -> Dict[str, Any]:
        """Get error summary for reporting."""
        return {
            "error_id": id(error_info),
            "error_type": error_info.error_type,
            "message": error_info.message,
            "severity": error_info.severity.value,
            "category": error_info.category.value,
            "operation": error_info.context.operation,
            "component": error_info.context.component,
            "timestamp": error_info.context.timestamp.isoformat(),
            "has_solution": error_info.solution is not None,
            "solution_description": error_info.solution.description if error_info.solution else None
        }
    
    def handle_and_format(self, exception: Exception, context: ErrorContext = None) -> str:
        """Handle error and return formatted message for user."""
        error_info = self.handle_error(exception, context)
        return self.format_error_message(error_info)


# Global instance for easy access
error_handler = BulletproofErrorHandler()


def handle_error_decorator(func):
    """Decorator to automatically handle errors in functions."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            context = ErrorContext(
                operation=func.__name__,
                component=func.__module__
            )
            error_info = error_handler.handle_error(e, context)
            formatted_message = error_handler.format_error_message(error_info)
            print(formatted_message)
            return None
    return wrapper
