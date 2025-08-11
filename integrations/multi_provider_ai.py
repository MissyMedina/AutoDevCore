#!/usr/bin/env python3
"""
AutoDevCore Multi-Provider AI Integration - BULLETPROOF EDITION
Supports OpenAI, Anthropic, Google AI, Cohere, Mistral, Perplexity, and GPT-OSS
"""

import asyncio
import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import aiohttp
import requests


class MultiProviderAI:
    """Multi-provider AI integration with intelligent model selection - BULLETPROOF"""

    def __init__(self, config_file: str = "config/api_config.json"):
        self.config_file = Path(config_file)
        self.config = self.load_config()
        self.session = None
        self.logger = logging.getLogger(__name__)

        # Provider configurations - BULLETPROOF COVERAGE
        self.providers = {
            "openai": {
                "name": "OpenAI",
                "icon": "🤖",
                "base_url": "https://api.openai.com/v1",
                "headers_template": lambda api_key: {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                "chat_endpoint": "/chat/completions",
                "models_endpoint": "/models",
                "models": ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo", "dall-e-3"],
                "strengths": ["code_generation", "creative_content", "reasoning"],
                "reliability": 0.95,
            },
            "anthropic": {
                "name": "Anthropic",
                "icon": "🧠",
                "base_url": "https://api.anthropic.com",
                "headers_template": lambda api_key: {
                    "x-api-key": api_key,
                    "Content-Type": "application/json",
                    "anthropic-version": "2023-06-01",
                },
                "chat_endpoint": "/v1/messages",
                "models_endpoint": "/v1/models",
                "models": ["claude-3-opus", "claude-3-sonnet", "claude-3-haiku", "claude-2.1"],
                "strengths": ["analysis", "safety", "research", "documentation"],
                "reliability": 0.92,
            },
            "google": {
                "name": "Google AI",
                "icon": "🔍",
                "base_url": "https://generativelanguage.googleapis.com",
                "headers_template": lambda api_key: {
                    "Content-Type": "application/json"
                },
                "chat_endpoint": "/v1beta/models/{model}:generateContent",
                "models_endpoint": "/v1beta/models",
                "models": ["gemini-pro", "gemini-pro-vision", "gemini-flash", "gemini-nano"],
                "strengths": ["multimodal", "fast_inference", "google_integration"],
                "reliability": 0.90,
            },
            "cohere": {
                "name": "Cohere",
                "icon": "🌟",
                "base_url": "https://api.cohere.ai",
                "headers_template": lambda api_key: {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                "chat_endpoint": "/v1/chat",
                "models_endpoint": "/v1/models",
                "models": ["command", "command-r", "command-r-plus", "embed-english-v3"],
                "strengths": ["rag_optimized", "embeddings", "cost_effective"],
                "reliability": 0.88,
            },
            "mistral": {
                "name": "Mistral AI",
                "icon": "🌪️",
                "base_url": "https://api.mistral.ai",
                "headers_template": lambda api_key: {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                "chat_endpoint": "/v1/chat/completions",
                "models_endpoint": "/v1/models",
                "models": ["mistral-large", "mistral-medium", "mistral-small", "mixtral-8x7b"],
                "strengths": ["open_source_friendly", "efficient", "cost_effective"],
                "reliability": 0.85,
            },
            "perplexity": {
                "name": "Perplexity",
                "icon": "🔍",
                "base_url": "https://api.perplexity.ai",
                "headers_template": lambda api_key: {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                "chat_endpoint": "/chat/completions",
                "models_endpoint": "/models",
                "models": ["llama-3.1-sonar-small", "llama-3.1-sonar-medium", "llama-3.1-sonar-large"],
                "strengths": ["web_search", "real_time_info", "research"],
                "reliability": 0.87,
            },
            "gpt-oss": {
                "name": "GPT-OSS",
                "icon": "🏠",
                "base_url": "http://localhost:11434",
                "headers_template": lambda api_key: {
                    "Content-Type": "application/json",
                },
                "chat_endpoint": "/api/generate",
                "models_endpoint": "/api/tags",
                "models": ["gpt-oss:20b", "gpt-oss:120b", "llama2", "codellama"],
                "strengths": ["offline", "free", "customizable", "privacy"],
                "reliability": 0.80,
            },
        }

        # Task-specific provider preferences - BULLETPROOF SELECTION
        self.task_preferences = {
            "code_generation": ["openai", "anthropic", "gpt-oss", "mistral"],
            "app_planning": ["anthropic", "openai", "google", "cohere"],
            "code_analysis": ["anthropic", "openai", "gpt-oss", "mistral"],
            "documentation": ["openai", "anthropic", "cohere", "google"],
            "research": ["perplexity", "anthropic", "google", "openai"],
            "creative_content": ["openai", "anthropic", "google", "mistral"],
            "security_audit": ["anthropic", "openai", "gpt-oss", "mistral"],
            "testing": ["openai", "anthropic", "gpt-oss", "cohere"],
        }

    def load_config(self) -> Dict[str, Any]:
        """Load API configuration with bulletproof error handling."""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            else:
                # Create default config
                default_config = {
                    "providers": {},
                    "default_provider": "gpt-oss",
                    "fallback_chain": ["gpt-oss", "openai", "anthropic", "google"],
                    "timeout": 60,
                    "max_retries": 3,
                    "cost_optimization": True,
                    "performance_tracking": True,
                }
                self.save_config(default_config)
                return default_config
        except Exception as e:
            self.logger.error(f"Failed to load config: {e}")
            return {"providers": {}, "default_provider": "gpt-oss"}

    def save_config(self, config: Dict[str, Any]) -> None:
        """Save API configuration with bulletproof error handling."""
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save config: {e}")

    async def test_provider_connection(self, provider_name: str) -> Dict[str, Any]:
        """Test provider connection with bulletproof error handling."""
        if provider_name not in self.providers:
            return {"success": False, "error": f"Unknown provider: {provider_name}"}

        provider_config = self.providers[provider_name]
        api_key = self.config.get("providers", {}).get(provider_name, {}).get("api_key")
        
        if not api_key and provider_name != "gpt-oss":
            return {"success": False, "error": f"No API key for {provider_name}"}

        try:
            headers = provider_config["headers_template"](api_key or "")
            
            # Test endpoint
            test_url = f"{provider_config['base_url']}{provider_config['models_endpoint']}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(test_url, headers=headers, timeout=10) as response:
                    if response.status == 200:
                        return {
                            "success": True,
                            "provider": provider_name,
                            "response_time": response.headers.get("x-response-time", "unknown"),
                            "models": provider_config["models"],
                            "strengths": provider_config["strengths"],
                        }
                    else:
                        return {
                            "success": False,
                            "error": f"HTTP {response.status}: {await response.text()}"
                        }
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def generate_response(
        self,
        prompt: str,
        task_type: str = "general",
        provider: Optional[str] = None,
        model: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate response with bulletproof fallback chain."""
        
        # Determine provider based on task and availability
        if not provider:
            provider = self._select_optimal_provider(task_type)
        
        # Try primary provider
        result = await self._call_provider(provider, prompt, model, **kwargs)
        if result["success"]:
            return result

        # BULLETPROOF FALLBACK CHAIN
        fallback_chain = self.config.get("fallback_chain", ["gpt-oss", "openai", "anthropic"])
        
        for fallback_provider in fallback_chain:
            if fallback_provider != provider:
                self.logger.info(f"Trying fallback provider: {fallback_provider}")
                result = await self._call_provider(fallback_provider, prompt, model, **kwargs)
                if result["success"]:
                    result["used_fallback"] = True
                    result["original_provider"] = provider
                    return result

        # FINAL FALLBACK - Return structured error response
        return {
            "success": False,
            "error": "All AI providers failed",
            "attempted_providers": [provider] + fallback_chain,
            "fallback_response": f"Unable to generate response. Please check your AI provider configurations and try again. Error: {result.get('error', 'Unknown error')}",
            "timestamp": datetime.now().isoformat(),
        }

    def _select_optimal_provider(self, task_type: str) -> str:
        """Select optimal provider based on task type and availability."""
        preferred_providers = self.task_preferences.get(task_type, ["gpt-oss", "openai", "anthropic"])
        
        # Check which providers have API keys configured
        configured_providers = []
        for provider in preferred_providers:
            if provider == "gpt-oss" or self.config.get("providers", {}).get(provider, {}).get("api_key"):
                configured_providers.append(provider)
        
        if configured_providers:
            return configured_providers[0]
        
        return "gpt-oss"  # Always available as local fallback

    async def _call_provider(
        self, provider_name: str, prompt: str, model: Optional[str] = None, **kwargs
    ) -> Dict[str, Any]:
        """Call specific provider with bulletproof error handling."""
        if provider_name not in self.providers:
            return {"success": False, "error": f"Unknown provider: {provider_name}"}

        provider_config = self.providers[provider_name]
        
        # Get API key (skip for gpt-oss)
        api_key = None
        if provider_name != "gpt-oss":
            api_key = self.config.get("providers", {}).get(provider_name, {}).get("api_key")
            if not api_key:
                return {"success": False, "error": f"No API key for {provider_name}"}

        # Select model
        if not model:
            model = provider_config["models"][0]

        try:
            start_time = time.time()
            
            if provider_name == "openai":
                response = await self._call_openai(provider_config, prompt, model, api_key, **kwargs)
            elif provider_name == "anthropic":
                response = await self._call_anthropic(provider_config, prompt, model, api_key, **kwargs)
            elif provider_name == "google":
                response = await self._call_google(provider_config, prompt, model, api_key, **kwargs)
            elif provider_name == "cohere":
                response = await self._call_cohere(provider_config, prompt, model, api_key, **kwargs)
            elif provider_name == "mistral":
                response = await self._call_mistral(provider_config, prompt, model, api_key, **kwargs)
            elif provider_name == "perplexity":
                response = await self._call_perplexity(provider_config, prompt, model, api_key, **kwargs)
            elif provider_name == "gpt-oss":
                response = await self._call_gpt_oss(provider_config, prompt, model, **kwargs)
            else:
                return {"success": False, "error": f"Unsupported provider: {provider_name}"}

            response_time = time.time() - start_time
            
            return {
                "success": True,
                "provider": provider_name,
                "model": model,
                "response": response,
                "response_time": response_time,
                "timestamp": datetime.now().isoformat(),
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _call_openai(self, config: Dict, prompt: str, model: str, api_key: str, **kwargs) -> str:
        """Call OpenAI API."""
        headers = config["headers_template"](api_key)
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": kwargs.get("max_tokens", 2000),
            "temperature": kwargs.get("temperature", 0.1),
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{config['base_url']}{config['chat_endpoint']}",
                headers=headers,
                json=payload,
                timeout=60
            ) as response:
                data = await response.json()
                return data["choices"][0]["message"]["content"]

    async def _call_anthropic(self, config: Dict, prompt: str, model: str, api_key: str, **kwargs) -> str:
        """Call Anthropic API."""
        headers = config["headers_template"](api_key)
        payload = {
            "model": model,
            "max_tokens": kwargs.get("max_tokens", 2000),
            "messages": [{"role": "user", "content": prompt}],
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{config['base_url']}{config['chat_endpoint']}",
                headers=headers,
                json=payload,
                timeout=60
            ) as response:
                data = await response.json()
                return data["content"][0]["text"]

    async def _call_google(self, config: Dict, prompt: str, model: str, api_key: str, **kwargs) -> str:
        """Call Google AI API."""
        headers = config["headers_template"](api_key)
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "maxOutputTokens": kwargs.get("max_tokens", 2000),
                "temperature": kwargs.get("temperature", 0.1),
            }
        }
        
        url = f"{config['base_url']}{config['chat_endpoint'].format(model=model)}?key={api_key}"
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload, timeout=60) as response:
                data = await response.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]

    async def _call_cohere(self, config: Dict, prompt: str, model: str, api_key: str, **kwargs) -> str:
        """Call Cohere API."""
        headers = config["headers_template"](api_key)
        payload = {
            "model": model,
            "message": prompt,
            "max_tokens": kwargs.get("max_tokens", 2000),
            "temperature": kwargs.get("temperature", 0.1),
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{config['base_url']}{config['chat_endpoint']}",
                headers=headers,
                json=payload,
                timeout=60
            ) as response:
                data = await response.json()
                return data["text"]

    async def _call_mistral(self, config: Dict, prompt: str, model: str, api_key: str, **kwargs) -> str:
        """Call Mistral AI API."""
        headers = config["headers_template"](api_key)
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": kwargs.get("max_tokens", 2000),
            "temperature": kwargs.get("temperature", 0.1),
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{config['base_url']}{config['chat_endpoint']}",
                headers=headers,
                json=payload,
                timeout=60
            ) as response:
                data = await response.json()
                return data["choices"][0]["message"]["content"]

    async def _call_perplexity(self, config: Dict, prompt: str, model: str, api_key: str, **kwargs) -> str:
        """Call Perplexity API."""
        headers = config["headers_template"](api_key)
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": kwargs.get("max_tokens", 2000),
            "temperature": kwargs.get("temperature", 0.1),
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{config['base_url']}{config['chat_endpoint']}",
                headers=headers,
                json=payload,
                timeout=60
            ) as response:
                data = await response.json()
                return data["choices"][0]["message"]["content"]

    async def _call_gpt_oss(self, config: Dict, prompt: str, model: str, **kwargs) -> str:
        """Call GPT-OSS (local Ollama)."""
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": kwargs.get("max_tokens", 2000),
                "temperature": kwargs.get("temperature", 0.1),
            }
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{config['base_url']}{config['chat_endpoint']}",
                json=payload,
                timeout=300
            ) as response:
                data = await response.json()
                return data["response"]

    def get_provider_status(self) -> Dict[str, Any]:
        """Get status of all providers."""
        status = {}
        for provider_name, provider_config in self.providers.items():
            has_api_key = (
                provider_name == "gpt-oss" or 
                bool(self.config.get("providers", {}).get(provider_name, {}).get("api_key"))
            )
            status[provider_name] = {
                "name": provider_config["name"],
                "icon": provider_config["icon"],
                "configured": has_api_key,
                "models": provider_config["models"],
                "strengths": provider_config["strengths"],
                "reliability": provider_config["reliability"],
            }
        return status

    def get_task_recommendations(self) -> Dict[str, List[str]]:
        """Get provider recommendations for different tasks."""
        return self.task_preferences


# Global instance for easy access
multi_provider_ai = MultiProviderAI()
