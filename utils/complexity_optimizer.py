#!/usr/bin/env python3
"""
Complexity Optimizer - Utilities to reduce cyclomatic complexity
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

class TaskType(Enum):
    """Task types for AI model selection."""

    APP_PLANNING = "app_planning"
    CODE_GENERATION = "code_generation"
    CODE_ANALYSIS = "code_analysis"
    SECURITY_AUDIT = "security_audit"
    DOCUMENTATION = "documentation"

class Priority(Enum):
    """Priority levels for tasks."""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class ModelConfig:
    """Configuration for AI model selection."""

    provider: str
    model: str
    max_tokens: int
    temperature: float
    cost_per_token: float

class ComplexityOptimizer:
    """Utilities to reduce cyclomatic complexity."""

    @staticmethod
    def extract_conditional_logic(
        condition: str, true_action: Callable, false_action: Callable
    ) -> Any:
        """Extract complex conditional logic into separate functions."""
        if condition:
            return true_action()
        return false_action()

    @staticmethod
    def create_strategy_pattern(conditions: List[Dict[str, Any]]) -> Callable:
        """Create strategy pattern for complex conditional logic."""

        def strategy_selector(input_data: Any) -> Any:
            for condition in conditions:
                if condition["predicate"](input_data):
                    return condition["action"](input_data)
            return conditions[-1]["default_action"](input_data)

        return strategy_selector

    @staticmethod
    def simplify_nested_conditions(conditions: List[Dict[str, Any]]) -> Callable:
        """Simplify nested if-elif-else chains."""

        def simplified_logic(input_data: Any) -> Any:
            for condition in conditions:
                if condition["check"](input_data):
                    return condition["result"]
            return conditions[-1]["default"]

        return simplified_logic

class ModelSelector:
    """Simplified model selection logic."""

    def __init__(self):
        self.models = {
            TaskType.APP_PLANNING: ModelConfig("openai", "gpt-4", 2000, 0.3, 0.03),
            TaskType.CODE_GENERATION: ModelConfig(
                "anthropic", "claude-3", 4000, 0.1, 0.015
            ),
            TaskType.CODE_ANALYSIS: ModelConfig(
                "gpt-oss", "gpt-oss:20b", 1000, 0.2, 0.001
            ),
            TaskType.SECURITY_AUDIT: ModelConfig("openai", "gpt-4", 1500, 0.1, 0.03),
            TaskType.DOCUMENTATION: ModelConfig(
                "anthropic", "claude-3", 3000, 0.2, 0.015
            ),
        }

    def select_model(
        self, task_type: TaskType, priority: Priority = Priority.NORMAL
    ) -> ModelConfig:
        """Select optimal model based on task type and priority."""
        base_config = self.models.get(task_type, self.models[TaskType.CODE_GENERATION])

        # Adjust based on priority
        if priority == Priority.HIGH:
            base_config = ModelConfig(
                base_config.provider,
                base_config.model,
                base_config.max_tokens * 2,
                base_config.temperature * 0.5,
                base_config.cost_per_token,
            )
        elif priority == Priority.LOW:
            base_config = ModelConfig(
                "gpt-oss",
                "gpt-oss:20b",
                base_config.max_tokens // 2,
                base_config.temperature * 1.5,
                0.001,
            )

        return base_config

class ErrorHandler:
    """Centralized error handling to reduce complexity."""

    @staticmethod
    def handle_ai_error(
        error: Exception, fallback_provider: str = "gpt-oss"
    ) -> Dict[str, Any]:
        """Handle AI-related errors with fallback."""
        error_types = {
            "timeout": {"action": "retry", "provider": fallback_provider},
            "rate_limit": {"action": "wait", "provider": fallback_provider},
            "invalid_response": {"action": "fallback", "provider": fallback_provider},
            "network_error": {"action": "retry", "provider": fallback_provider},
        }

        error_type = type(error).__name__.lower()
        strategy = error_types.get(
            error_type, {"action": "fallback", "provider": fallback_provider}
        )

        return {
            "error": str(error),
            "type": error_type,
            "action": strategy["action"],
            "fallback_provider": strategy["provider"],
            "success": False,
        }

    @staticmethod
    def handle_validation_error(
        field: str, value: Any, expected_type: str
    ) -> Dict[str, Any]:
        """Handle validation errors consistently."""
        return {
            "error": f"Invalid {field}: expected {expected_type}, got {type(value).__name__}",
            "field": field,
            "value": str(value),
            "expected_type": expected_type,
            "success": False,
        }

class CacheManager:
    """Simplified caching logic."""

    def __init__(self):
        self.cache = {}
        self.ttl = {}

    def get(self, key: str, default: Any = None) -> Any:
        """Get value from cache with TTL check."""
        if key in self.cache and self._is_valid(key):
            return self.cache[key]
        return default

    def set(self, key: str, value: Any, ttl_seconds: int = 3600) -> None:
        """Set value in cache with TTL."""
        self.cache[key] = value
        self.ttl[key] = ttl_seconds

    def _is_valid(self, key: str) -> bool:
        """Check if cache entry is still valid."""
        return key in self.ttl and self.ttl[key] > 0

# Global instances for easy access
complexity_optimizer = ComplexityOptimizer()
model_selector = ModelSelector()
error_handler = ErrorHandler()
cache_manager = CacheManager()
