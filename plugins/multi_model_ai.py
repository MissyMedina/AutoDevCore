#!/usr/bin/env python3
"""
Multi-Model AI Integration - Intelligent AI model selection and orchestration
"""

import os
import time
import json
import asyncio
import aiohttp
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import logging


class ModelProvider(Enum):
    """Supported AI model providers."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GPT_OSS = "gpt-oss"
    FALLBACK = "fallback"


class TaskType(Enum):
    """Types of AI tasks for model selection."""
    CODE_GENERATION = "code_generation"
    APP_PLANNING = "app_planning"
    ANALYSIS = "analysis"
    SCORING = "scoring"
    DOCUMENTATION = "documentation"


@dataclass
class ModelConfig:
    """Configuration for an AI model."""
    provider: ModelProvider
    model_name: str
    api_key_env: str
    base_url: str
    max_tokens: int
    temperature: float
    timeout: int
    cost_per_1k_tokens: float
    reliability_score: float
    speed_score: float
    quality_score: float
    supported_tasks: List[TaskType]
    is_available: bool = True
    last_used: Optional[datetime] = None
    success_rate: float = 0.0
    avg_response_time: float = 0.0


@dataclass
class AIRequest:
    """AI request configuration."""
    prompt: str
    task_type: TaskType
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    timeout: Optional[int] = None
    priority: str = "normal"  # low, normal, high
    fallback_required: bool = True


@dataclass
class AIResponse:
    """AI response structure."""
    content: str
    model_used: str
    provider: ModelProvider
    tokens_used: int
    response_time: float
    cost: float
    success: bool
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class ModelHealthChecker:
    """Check health and availability of AI models."""
    
    def __init__(self):
        self.health_cache = {}
        self.cache_duration = timedelta(minutes=5)
    
    async def check_model_health(self, model_config: ModelConfig) -> bool:
        """Check if a model is healthy and available."""
        cache_key = f"{model_config.provider.value}_{model_config.model_name}"
        
        # Check cache first
        if cache_key in self.health_cache:
            last_check, is_healthy = self.health_cache[cache_key]
            if datetime.now() - last_check < self.cache_duration:
                return is_healthy
        
        try:
            # Simple health check based on provider
            if model_config.provider == ModelProvider.OPENAI:
                is_healthy = await self._check_openai_health(model_config)
            elif model_config.provider == ModelProvider.ANTHROPIC:
                is_healthy = await self._check_anthropic_health(model_config)
            elif model_config.provider == ModelProvider.GPT_OSS:
                is_healthy = await self._check_gpt_oss_health(model_config)
            else:
                is_healthy = True  # Fallback is always available
            
            # Update cache
            self.health_cache[cache_key] = (datetime.now(), is_healthy)
            return is_healthy
            
        except Exception as e:
            logging.warning(f"Health check failed for {model_config.model_name}: {e}")
            self.health_cache[cache_key] = (datetime.now(), False)
            return False
    
    async def _check_openai_health(self, model_config: ModelConfig) -> bool:
        """Check OpenAI model health."""
        api_key = os.getenv(model_config.api_key_env)
        if not api_key:
            return False
        
        try:
            async with aiohttp.ClientSession() as session:
                headers = {"Authorization": f"Bearer {api_key}"}
                async with session.get(
                    "https://api.openai.com/v1/models",
                    headers=headers,
                    timeout=10
                ) as response:
                    return response.status == 200
        except:
            return False
    
    async def _check_anthropic_health(self, model_config: ModelConfig) -> bool:
        """Check Anthropic model health."""
        api_key = os.getenv(model_config.api_key_env)
        if not api_key:
            return False
        
        try:
            async with aiohttp.ClientSession() as session:
                headers = {"x-api-key": api_key}
                async with session.get(
                    "https://api.anthropic.com/v1/models",
                    headers=headers,
                    timeout=10
                ) as response:
                    return response.status == 200
        except:
            return False
    
    async def _check_gpt_oss_health(self, model_config: ModelConfig) -> bool:
        """Check GPT-OSS model health."""
        try:
            import requests
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                return any(model_config.model_name in model.get("name", "") for model in models)
            return False
        except:
            return False


class ModelSelector:
    """Intelligent model selection based on task and performance."""
    
    def __init__(self):
        self.performance_history = {}
        self.task_preferences = {
            TaskType.CODE_GENERATION: [ModelProvider.OPENAI, ModelProvider.ANTHROPIC, ModelProvider.GPT_OSS],
            TaskType.APP_PLANNING: [ModelProvider.ANTHROPIC, ModelProvider.OPENAI, ModelProvider.GPT_OSS],
            TaskType.ANALYSIS: [ModelProvider.ANTHROPIC, ModelProvider.OPENAI, ModelProvider.GPT_OSS],
            TaskType.SCORING: [ModelProvider.GPT_OSS, ModelProvider.OPENAI, ModelProvider.ANTHROPIC],
            TaskType.DOCUMENTATION: [ModelProvider.OPENAI, ModelProvider.ANTHROPIC, ModelProvider.GPT_OSS]
        }
    
    def select_optimal_model(self, 
                           available_models: List[ModelConfig], 
                           task_type: TaskType,
                           priority: str = "normal") -> Optional[ModelConfig]:
        """Select the optimal model for a given task."""
        if not available_models:
            return None
        
        # Filter models that support this task
        supported_models = [
            model for model in available_models 
            if task_type in model.supported_tasks and model.is_available
        ]
        
        if not supported_models:
            return None
        
        # Get task preferences
        task_prefs = self.task_preferences.get(task_type, [])
        
        # Score models based on multiple factors
        scored_models = []
        for model in supported_models:
            score = self._calculate_model_score(model, task_type, priority, task_prefs)
            scored_models.append((model, score))
        
        # Sort by score (highest first)
        scored_models.sort(key=lambda x: x[1], reverse=True)
        
        return scored_models[0][0] if scored_models else None
    
    def _calculate_model_score(self, 
                              model: ModelConfig, 
                              task_type: TaskType, 
                              priority: str,
                              task_prefs: List[ModelProvider]) -> float:
        """Calculate a score for model selection."""
        score = 0.0
        
        # Base score from model configuration
        score += model.reliability_score * 0.3
        score += model.quality_score * 0.3
        score += model.speed_score * 0.2
        
        # Task preference bonus
        if model.provider in task_prefs:
            preference_index = task_prefs.index(model.provider)
            score += (len(task_prefs) - preference_index) * 0.1
        
        # Performance history bonus
        history_key = f"{model.provider.value}_{model.model_name}_{task_type.value}"
        if history_key in self.performance_history:
            history = self.performance_history[history_key]
            score += history.get("success_rate", 0.0) * 0.2
            score -= history.get("avg_response_time", 10.0) * 0.01
        
        # Priority adjustments
        if priority == "high":
            score += model.quality_score * 0.2
        elif priority == "low":
            score += model.speed_score * 0.2
        
        # Cost consideration (lower cost = higher score)
        score -= model.cost_per_1k_tokens * 0.01
        
        return max(0.0, score)
    
    def record_performance(self, 
                          model: ModelConfig, 
                          task_type: TaskType, 
                          response_time: float, 
                          success: bool):
        """Record performance metrics for model selection."""
        history_key = f"{model.provider.value}_{model.model_name}_{task_type.value}"
        
        if history_key not in self.performance_history:
            self.performance_history[history_key] = {
                "total_requests": 0,
                "successful_requests": 0,
                "total_response_time": 0.0,
                "success_rate": 0.0,
                "avg_response_time": 0.0
            }
        
        history = self.performance_history[history_key]
        history["total_requests"] += 1
        history["total_response_time"] += response_time
        
        if success:
            history["successful_requests"] += 1
        
        history["success_rate"] = history["successful_requests"] / history["total_requests"]
        history["avg_response_time"] = history["total_response_time"] / history["total_requests"]


class MultiModelAI:
    """Multi-model AI integration with intelligent selection and fallback."""
    
    def __init__(self):
        self.models = self._initialize_models()
        self.health_checker = ModelHealthChecker()
        self.model_selector = ModelSelector()
        self.session = None
    
    def _initialize_models(self) -> List[ModelConfig]:
        """Initialize available AI models."""
        return [
            ModelConfig(
                provider=ModelProvider.OPENAI,
                model_name="gpt-4",
                api_key_env="OPENAI_API_KEY",
                base_url="https://api.openai.com/v1",
                max_tokens=4000,
                temperature=0.1,
                timeout=60,
                cost_per_1k_tokens=0.03,
                reliability_score=0.95,
                speed_score=0.8,
                quality_score=0.9,
                supported_tasks=[TaskType.CODE_GENERATION, TaskType.APP_PLANNING, 
                               TaskType.ANALYSIS, TaskType.DOCUMENTATION]
            ),
            ModelConfig(
                provider=ModelProvider.ANTHROPIC,
                model_name="claude-3-sonnet-20240229",
                api_key_env="ANTHROPIC_API_KEY",
                base_url="https://api.anthropic.com/v1",
                max_tokens=4000,
                temperature=0.1,
                timeout=60,
                cost_per_1k_tokens=0.015,
                reliability_score=0.9,
                speed_score=0.7,
                quality_score=0.95,
                supported_tasks=[TaskType.CODE_GENERATION, TaskType.APP_PLANNING, 
                               TaskType.ANALYSIS, TaskType.DOCUMENTATION]
            ),
            ModelConfig(
                provider=ModelProvider.GPT_OSS,
                model_name="gpt-oss:20b",
                api_key_env="",
                base_url="http://localhost:11434",
                max_tokens=2048,
                temperature=0.1,
                timeout=300,
                cost_per_1k_tokens=0.0,
                reliability_score=0.8,
                speed_score=0.6,
                quality_score=0.7,
                supported_tasks=[TaskType.CODE_GENERATION, TaskType.APP_PLANNING, 
                               TaskType.ANALYSIS, TaskType.SCORING, TaskType.DOCUMENTATION]
            ),
            ModelConfig(
                provider=ModelProvider.FALLBACK,
                model_name="fallback",
                api_key_env="",
                base_url="",
                max_tokens=100,
                temperature=0.0,
                timeout=5,
                cost_per_1k_tokens=0.0,
                reliability_score=1.0,
                speed_score=1.0,
                quality_score=0.5,
                supported_tasks=[TaskType.CODE_GENERATION, TaskType.APP_PLANNING, 
                               TaskType.ANALYSIS, TaskType.SCORING, TaskType.DOCUMENTATION]
            )
        ]
    
    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()
    
    async def generate(self, request: AIRequest) -> AIResponse:
        """Generate AI response using optimal model selection."""
        start_time = time.time()
        
        # Check model health
        available_models = []
        for model in self.models:
            if await self.health_checker.check_model_health(model):
                model.is_available = True
                available_models.append(model)
            else:
                model.is_available = False
        
        # Select optimal model
        selected_model = self.model_selector.select_optimal_model(
            available_models, request.task_type, request.priority
        )
        
        if not selected_model:
            # Use fallback model
            selected_model = next(m for m in self.models if m.provider == ModelProvider.FALLBACK)
        
        # Generate response
        try:
            response = await self._generate_with_model(selected_model, request)
            
            # Record performance
            response_time = time.time() - start_time
            self.model_selector.record_performance(
                selected_model, request.task_type, response_time, response.success
            )
            
            return response
            
        except Exception as e:
            # Try fallback if not already using it
            if selected_model.provider != ModelProvider.FALLBACK and request.fallback_required:
                fallback_model = next(m for m in self.models if m.provider == ModelProvider.FALLBACK)
                return await self._generate_with_model(fallback_model, request)
            else:
                raise e
    
    async def _generate_with_model(self, model: ModelConfig, request: AIRequest) -> AIResponse:
        """Generate response using a specific model."""
        start_time = time.time()
        
        try:
            if model.provider == ModelProvider.OPENAI:
                content, tokens_used = await self._call_openai(model, request)
            elif model.provider == ModelProvider.ANTHROPIC:
                content, tokens_used = await self._call_anthropic(model, request)
            elif model.provider == ModelProvider.GPT_OSS:
                content, tokens_used = await self._call_gpt_oss(model, request)
            elif model.provider == ModelProvider.FALLBACK:
                content, tokens_used = await self._call_fallback(model, request)
            else:
                raise ValueError(f"Unsupported model provider: {model.provider}")
            
            response_time = time.time() - start_time
            cost = (tokens_used / 1000) * model.cost_per_1k_tokens
            
            return AIResponse(
                content=content,
                model_used=model.model_name,
                provider=model.provider,
                tokens_used=tokens_used,
                response_time=response_time,
                cost=cost,
                success=True,
                metadata={"model_config": model.model_name}
            )
            
        except Exception as e:
            response_time = time.time() - start_time
            return AIResponse(
                content=f"Error: {str(e)}",
                model_used=model.model_name,
                provider=model.provider,
                tokens_used=0,
                response_time=response_time,
                cost=0.0,
                success=False,
                error_message=str(e)
            )
    
    async def _call_openai(self, model: ModelConfig, request: AIRequest) -> tuple[str, int]:
        """Call OpenAI API."""
        api_key = os.getenv(model.api_key_env)
        if not api_key:
            raise ValueError("OpenAI API key not found")
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": model.model_name,
            "messages": [{"role": "user", "content": request.prompt}],
            "max_tokens": request.max_tokens or model.max_tokens,
            "temperature": request.temperature or model.temperature
        }
        
        async with self.session.post(
            f"{model.base_url}/chat/completions",
            headers=headers,
            json=data,
            timeout=request.timeout or model.timeout
        ) as response:
            if response.status != 200:
                raise Exception(f"OpenAI API error: {response.status}")
            
            result = await response.json()
            content = result["choices"][0]["message"]["content"]
            tokens_used = result["usage"]["total_tokens"]
            
            return content, tokens_used
    
    async def _call_anthropic(self, model: ModelConfig, request: AIRequest) -> tuple[str, int]:
        """Call Anthropic API."""
        api_key = os.getenv(model.api_key_env)
        if not api_key:
            raise ValueError("Anthropic API key not found")
        
        headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        data = {
            "model": model.model_name,
            "max_tokens": request.max_tokens or model.max_tokens,
            "temperature": request.temperature or model.temperature,
            "messages": [{"role": "user", "content": request.prompt}]
        }
        
        async with self.session.post(
            f"{model.base_url}/messages",
            headers=headers,
            json=data,
            timeout=request.timeout or model.timeout
        ) as response:
            if response.status != 200:
                raise Exception(f"Anthropic API error: {response.status}")
            
            result = await response.json()
            content = result["content"][0]["text"]
            tokens_used = result["usage"]["input_tokens"] + result["usage"]["output_tokens"]
            
            return content, tokens_used
    
    async def _call_gpt_oss(self, model: ModelConfig, request: AIRequest) -> tuple[str, int]:
        """Call GPT-OSS (Ollama) API."""
        import requests
        
        data = {
            "model": model.model_name,
            "prompt": request.prompt,
            "stream": False,
            "options": {
                "num_predict": request.max_tokens or model.max_tokens,
                "temperature": request.temperature or model.temperature
            }
        }
        
        response = requests.post(
            f"{model.base_url}/api/generate",
            json=data,
            timeout=request.timeout or model.timeout
        )
        
        if response.status_code != 200:
            raise Exception(f"GPT-OSS API error: {response.status_code}")
        
        result = response.json()
        content = result["response"]
        tokens_used = len(request.prompt.split()) + len(content.split())  # Approximate
        
        return content, tokens_used
    
    async def _call_fallback(self, model: ModelConfig, request: AIRequest) -> tuple[str, int]:
        """Call fallback model with pre-defined responses."""
        fallback_responses = {
            TaskType.CODE_GENERATION: "# Generated code placeholder\n# This is a fallback response",
            TaskType.APP_PLANNING: "Fallback app plan: Basic application structure with standard features",
            TaskType.ANALYSIS: "Fallback analysis: Standard code analysis with basic recommendations",
            TaskType.SCORING: "Fallback score: 75/100 - Standard application quality",
            TaskType.DOCUMENTATION: "# Fallback Documentation\nBasic documentation template"
        }
        
        content = fallback_responses.get(request.task_type, "Fallback response")
        tokens_used = len(content.split())
        
        return content, tokens_used
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get comprehensive performance report."""
        return {
            "model_performance": self.model_selector.performance_history,
            "model_health": {
                model.model_name: model.is_available 
                for model in self.models
            },
            "task_preferences": {
                task.value: [p.value for p in prefs]
                for task, prefs in self.model_selector.task_preferences.items()
            },
            "total_models": len(self.models),
            "available_models": len([m for m in self.models if m.is_available])
        }


# Global instance for easy access
multi_model_ai = MultiModelAI()


async def generate_ai_response(prompt: str, 
                             task_type: TaskType, 
                             **kwargs) -> AIResponse:
    """Convenience function for generating AI responses."""
    request = AIRequest(prompt=prompt, task_type=task_type, **kwargs)
    
    async with multi_model_ai as ai:
        return await ai.generate(request)


def run(context=None):
    """Plugin entry point for testing."""
    async def test_multi_model():
        # Test the multi-model AI system
        prompt = "Generate a simple Python function to calculate fibonacci numbers"
        
        try:
            response = await generate_ai_response(
                prompt=prompt,
                task_type=TaskType.CODE_GENERATION,
                priority="normal"
            )
            
            return {
                "status": "success",
                "message": "Multi-model AI test completed",
                "data": {
                    "model_used": response.model_used,
                    "provider": response.provider.value,
                    "response_time": response.response_time,
                    "cost": response.cost,
                    "success": response.success,
                    "content_preview": response.content[:100] + "..." if len(response.content) > 100 else response.content
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Multi-model AI test failed: {e}",
                "data": {}
            }
    
    # Run the async test
    import asyncio
    return asyncio.run(test_multi_model())
