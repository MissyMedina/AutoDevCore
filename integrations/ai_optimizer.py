#!/usr/bin/env python3
"""
AI Optimizer - Advanced AI model optimization with smart fallbacks
"""

import asyncio
import json
import time
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

class ModelType(Enum):
    """Available AI model types."""

    GPT_OSS_20B = "gpt-oss:20b"
    GPT_OSS_120B = "gpt-oss:120b"
    FALLBACK = "fallback"

@dataclass
class ModelConfig:
    """Configuration for an AI model."""

    name: str
    type: ModelType
    base_url: str
    timeout: int
    max_tokens: int
    temperature: float
    priority: int
    cost_per_token: float
    reliability_score: float

class AIOptimizer:
    """Advanced AI optimizer with smart fallbacks and model selection."""

    def __init__(self):
        self.models = {
            ModelType.GPT_OSS_20B: ModelConfig(
                name="GPT-OSS 20B",
                type=ModelType.GPT_OSS_20B,
                base_url="http://localhost:11434",
                timeout=300,
                max_tokens=256,
                temperature=0.1,
                priority=1,
                cost_per_token=0.001,
                reliability_score=0.8,
            ),
            ModelType.GPT_OSS_120B: ModelConfig(
                name="GPT-OSS 120B",
                type=ModelType.GPT_OSS_120B,
                base_url="http://localhost:11434",
                timeout=600,
                max_tokens=512,
                temperature=0.3,
                priority=2,
                cost_per_token=0.002,
                reliability_score=0.9,
            ),
            ModelType.FALLBACK: ModelConfig(
                name="Fallback",
                type=ModelType.FALLBACK,
                base_url="",
                timeout=5,
                max_tokens=100,
                temperature=0.0,
                priority=3,
                cost_per_token=0.0,
                reliability_score=1.0,
            ),
        }

        self.model_performance = {}
        self.request_history = []
        self.fallback_responses = {
            "app_plan": {
                "app_name": "AutoDevApp",
                "description": "AI-generated application",
                "features": ["User authentication", "CRUD operations", "API endpoints"],
                "tech_stack": {"backend": "Python/FastAPI", "database": "SQLite"},
                "architecture": "MVC pattern",
                "database_schema": [],
                "api_endpoints": [],
                "ui_components": [],
                "deployment": "Docker",
            },
            "code_generation": "# Generated code placeholder\n# This is a fallback response",
            "analysis": {
                "analysis_type": "general",
                "findings": ["Code structure is standard"],
                "recommendations": ["Follow best practices"],
                "score": 75,
            },
        }

    def get_optimal_model(
        self, task_type: str, complexity: str = "medium"
    ) -> ModelConfig:
        """Select the optimal model based on task type and complexity."""
        if complexity == "simple":
            return self.models[ModelType.GPT_OSS_20B]
        elif complexity == "complex":
            return self.models[ModelType.GPT_OSS_120B]
        else:
            # Use performance history to select best model
            return self._select_best_performing_model(task_type)

    def _select_best_performing_model(self, task_type: str) -> ModelConfig:
        """Select the best performing model based on historical data."""
        if task_type not in self.model_performance:
            return self.models[ModelType.GPT_OSS_20B]

        performance = self.model_performance[task_type]
        best_model = None
        best_score = 0

        for model_type, stats in performance.items():
            if model_type in self.models:
                # Calculate score based on success rate and speed
                success_rate = stats.get("success_rate", 0)
                avg_time = stats.get("avg_time", 10)
                score = success_rate / (avg_time + 1)  # Avoid division by zero

                if score > best_score:
                    best_score = score
                    best_model = self.models[model_type]

        return best_model or self.models[ModelType.GPT_OSS_20B]

    def record_performance(
        self, model_type: ModelType, task_type: str, duration: float, success: bool
    ):
        """Record performance metrics for model selection."""
        if task_type not in self.model_performance:
            self.model_performance[task_type] = {}

        if model_type not in self.model_performance[task_type]:
            self.model_performance[task_type][model_type] = {
                "total_requests": 0,
                "successful_requests": 0,
                "total_time": 0,
                "success_rate": 0,
                "avg_time": 0,
            }

        stats = self.model_performance[task_type][model_type]
        stats["total_requests"] += 1
        stats["total_time"] += duration

        if success:
            stats["successful_requests"] += 1

        stats["success_rate"] = stats["successful_requests"] / stats["total_requests"]
        stats["avg_time"] = stats["total_time"] / stats["total_requests"]

    def get_fallback_response(self, task_type: str) -> Any:
        """Get a fallback response for when AI models fail."""
        return self.fallback_responses.get(task_type, "Fallback response")

    def optimize_prompt(self, prompt: str, task_type: str) -> str:
        """Optimize prompts for better performance."""
        optimizations = {
            "app_plan": self._optimize_app_plan_prompt,
            "code_generation": self._optimize_code_prompt,
            "analysis": self._optimize_analysis_prompt,
        }

        optimizer = optimizations.get(task_type, lambda p: p)
        return optimizer(prompt)

    def _optimize_app_plan_prompt(self, prompt: str) -> str:
        """Optimize app plan prompts for faster generation."""
        return f"""
Create a concise application plan for: {prompt}

Provide a JSON response with only essential fields:
- app_name (string)
- description (string)
- features (list, max 5 items)
- tech_stack (dict with backend, database only)
- architecture (string, one line)
"""

    def _optimize_code_prompt(self, prompt: str) -> str:
        """Optimize code generation prompts."""
        return f"""
Generate minimal, functional code for: {prompt}

Requirements:
- Focus on core functionality only
- Use standard libraries when possible
- Keep code concise and readable
- Include basic error handling
"""

    def _optimize_analysis_prompt(self, prompt: str) -> str:
        """Optimize analysis prompts."""
        return f"""
Analyze the following code briefly: {prompt[:1000]}

Provide a concise JSON response with:
- analysis_type (string)
- findings (list, max 3 items)
- recommendations (list, max 2 items)
- score (0-100)
"""

    def get_performance_report(self) -> Dict[str, Any]:
        """Generate a performance report."""
        return {
            "model_performance": self.model_performance,
            "total_requests": len(self.request_history),
            "optimization_stats": {
                "prompts_optimized": sum(
                    1 for req in self.request_history if req.get("optimized")
                ),
                "fallbacks_used": sum(
                    1 for req in self.request_history if req.get("fallback")
                ),
                "avg_response_time": (
                    sum(req.get("duration", 0) for req in self.request_history)
                    / len(self.request_history)
                    if self.request_history
                    else 0
                ),
            },
        }

# Global AI optimizer instance
ai_optimizer = AIOptimizer()

def optimize_ai_request(task_type: str, complexity: str = "medium"):
    """Decorator to optimize AI requests with smart fallbacks."""

    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()

            # Get optimal model
            model_config = ai_optimizer.get_optimal_model(task_type, complexity)

            # Optimize prompt if present
            if "prompt" in kwargs:
                kwargs["prompt"] = ai_optimizer.optimize_prompt(
                    kwargs["prompt"], task_type
                )

            try:
                # Try with optimal model
                result = func(*args, **kwargs)
                duration = time.time() - start_time

                # Record success
                ai_optimizer.record_performance(
                    model_config.type, task_type, duration, True
                )
                ai_optimizer.request_history.append(
                    {
                        "task_type": task_type,
                        "model": model_config.name,
                        "duration": duration,
                        "success": True,
                        "optimized": True,
                        "fallback": False,
                    }
                )

                return result

            except Exception as e:
                duration = time.time() - start_time

                # Record failure
                ai_optimizer.record_performance(
                    model_config.type, task_type, duration, False
                )

                # Try fallback
                try:
                    fallback_result = ai_optimizer.get_fallback_response(task_type)
                    ai_optimizer.request_history.append(
                        {
                            "task_type": task_type,
                            "model": "fallback",
                            "duration": duration,
                            "success": True,
                            "optimized": False,
                            "fallback": True,
                        }
                    )
                    return fallback_result
                except:
                    # Final fallback
                    ai_optimizer.request_history.append(
                        {
                            "task_type": task_type,
                            "model": "fallback",
                            "duration": duration,
                            "success": False,
                            "optimized": False,
                            "fallback": True,
                        }
                    )
                    raise e

        return wrapper

    return decorator
