"""
GPT-OSS Integration for AutoDevCore
"""

import hashlib
import json
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

class GPTOSSClient:
    """Client for interacting with GPT-OSS models via Ollama."""

    def __init__(
        self, base_url: str = "http://localhost:11434", model: str = "gpt-oss:20b"
    ):
        self.base_url = base_url
        self.model = model
        self.session = requests.Session()
        self.session.timeout = 300  # 5 minutes timeout

        # Performance optimizations
        self.cache_dir = Path(".cache/gpt_oss")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_ttl = 3600  # 1 hour cache TTL

        # Request optimization parameters - Optimized for speed
        self.optimization_params = {
            "num_ctx": 2048,  # Further reduced context window for speed
            "num_thread": 4,  # Reduced threads for faster response
            "temperature": 0.1,  # Very low temperature for consistency
            "top_p": 0.8,  # More focused sampling
            "top_k": 20,  # Reduced top-k for speed
            "repeat_penalty": 1.05,  # Minimal repetition penalty
            "num_predict": 256,  # Shorter responses for speed
        }

        # Performance monitoring
        self.request_times = []
        self.cache_hits = 0
        self.cache_misses = 0

    def _get_cache_key(self, prompt: str, **kwargs) -> str:
        """Generate a cache key for the request."""
        cache_data = {"prompt": prompt, "model": self.model, "params": kwargs}
        cache_str = json.dumps(cache_data, sort_keys=True)
        return hashlib.md5(cache_str.encode(), usedforsecurity=False).hexdigest()

    def _get_cache_path(self, cache_key: str) -> Path:
        """Get the cache file path."""
        return self.cache_dir / f"{cache_key}.json"

    def _load_from_cache(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Load response from cache if valid."""
        cache_path = self._get_cache_path(cache_key)

        if not cache_path.exists():
            return None

        try:
            # Check if cache is still valid
            if time.time() - cache_path.stat().st_mtime > self.cache_ttl:
                cache_path.unlink()  # Remove expired cache
                return None

            with open(cache_path, "r") as f:
                cached_data = json.load(f)
                return cached_data

        except Exception:
            # If cache is corrupted, remove it
            if cache_path.exists():
                cache_path.unlink()
            return None

    def _save_to_cache(self, cache_key: str, response: Dict[str, Any]):
        """Save response to cache."""
        try:
            cache_path = self._get_cache_path(cache_key)
            with open(cache_path, "w") as f:
                json.dump(response, f)
        except Exception:
            # Silently fail if caching fails
            pass

    def _make_request(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Make a request to Ollama with caching and optimization."""

        import time

        start_time = time.time()

        # Generate cache key
        cache_key = self._get_cache_key(prompt, **kwargs)

        # Try to load from cache first
        cached_response = self._load_from_cache(cache_key)
        if cached_response:
            self.cache_hits += 1
            return cached_response

        self.cache_misses += 1

        # Prepare request with optimization parameters
        request_data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            **self.optimization_params,
            **kwargs,
        }

        try:
            response = self.session.post(
                f"{self.base_url}/api/generate", json=request_data, timeout=300
            )
            response.raise_for_status()

            result = response.json()

            # Track performance
            end_time = time.time()
            self.request_times.append(end_time - start_time)

            # Save to cache
            self._save_to_cache(cache_key, result)

            return result

        except requests.exceptions.Timeout:
            # Return a fallback response instead of crashing
            return {
                "model": self.model,
                "created_at": time.time(),
                "response": "Model timeout - using fallback response",
                "done": True,
                "message": {
                    "content": "Model timeout - using fallback response",
                    "role": "assistant",
                },
            }
        except requests.exceptions.RequestException as e:
            # Return a fallback response instead of crashing
            return {
                "model": self.model,
                "created_at": time.time(),
                "response": f"Request failed: {e}",
                "done": True,
                "message": {"content": f"Request failed: {e}", "role": "assistant"},
            }

    def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate text using GPT-OSS with caching."""
        try:
            return self._make_request(prompt, **kwargs)
        except Exception as e:
            # Return a fallback response instead of crashing
            return {
                "model": self.model,
                "created_at": time.time(),
                "response": f"Error: {str(e)}",
                "done": True,
                "message": {"content": f"Error: {str(e)}", "role": "assistant"},
            }

    def generate_with_tools(
        self, prompt: str, tools: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate text with tool calling support."""
        # For now, return a simple response since tool calling is complex
        return self.generate(prompt)

    def analyze_code(self, code: str, analysis_type: str = "general") -> Dict[str, Any]:
        """Analyze code with caching."""
        prompt = f"""
        Analyze the following code for {analysis_type}:

        {code[:2000]}

        Provide a JSON response with:
        - analysis_type (string)
        - findings (list)
        - recommendations (list)
        - score (0-100)
        """

        try:
            response = self._make_request(prompt)
            content = response.get("response", "")

            # Try to extract JSON from response
            try:
                start = content.find("{")
                end = content.rfind("}") + 1
                if start != -1 and end != 0:
                    json_str = content[start:end]
                    return json.loads(json_str)
                else:
                    return {"error": "Could not parse response"}
            except:
                return {"error": "Invalid JSON response"}

        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}

    def generate_app_plan(self, idea: str) -> Dict[str, Any]:
        """Generate an application plan with caching."""
        prompt = f"""
        Create a detailed application plan for: {idea}

        Provide a JSON response with:
        - app_name (string)
        - description (string)
        - features (list)
        - tech_stack (dict with backend, frontend, database)
        - architecture (string)
        - database_schema (list)
        - api_endpoints (list)
        - ui_components (list)
        - deployment (string)
        """

        try:
            response = self._make_request(prompt)
            content = response.get("response", "")

            # Try to extract JSON from response
            try:
                start = content.find("{")
                end = content.rfind("}") + 1
                if start != -1 and end != 0:
                    json_str = content[start:end]
                    return json.loads(json_str)
                else:
                    return {"error": "Could not parse response"}
            except:
                return {"error": "Invalid JSON response"}

        except Exception as e:
            return {"error": f"Plan generation failed: {str(e)}"}

    def generate_code(self, prompt: str, language: str = "python") -> str:
        """Generate code with caching."""
        full_prompt = f"""
        Generate {language} code for:

        {prompt}

        Provide only the code, no explanations.
        """

        try:
            response = self._make_request(full_prompt)
            return response.get("response", "")
        except Exception as e:
            return f"# Error generating code: {str(e)}"

    def score_application(
        self, app_description: str, criteria: List[str]
    ) -> Dict[str, Any]:
        """Score an application against criteria with caching."""
        prompt = f"""
        Score this application: {app_description}

        Against these criteria: {', '.join(criteria)}

        Provide a JSON response with:
        - overall_score (0-100)
        - category_scores (dict)
        - strengths (list)
        - weaknesses (list)
        - recommendations (list)
        """

        try:
            response = self._make_request(prompt)
            content = response.get("response", "")

            # Try to extract JSON from response
            try:
                start = content.find("{")
                end = content.rfind("}") + 1
                if start != -1 and end != 0:
                    json_str = content[start:end]
                    return json.loads(json_str)
                else:
                    return {"error": "Could not parse response"}
            except:
                return {"error": "Invalid JSON response"}

        except Exception as e:
            return {"error": f"Scoring failed: {str(e)}"}

    def clear_cache(self):
        """Clear all cached responses."""
        try:
            for cache_file in self.cache_dir.glob("*.json"):
                cache_file.unlink()
        except Exception:
            pass

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics and performance metrics."""
        try:
            cache_files = list(self.cache_dir.glob("*.json"))
            total_size = sum(f.stat().st_size for f in cache_files)

            # Calculate performance metrics
            avg_request_time = (
                sum(self.request_times) / len(self.request_times)
                if self.request_times
                else 0
            )
            cache_hit_rate = (
                self.cache_hits / (self.cache_hits + self.cache_misses)
                if (self.cache_hits + self.cache_misses) > 0
                else 0
            )

            return {
                "cache_files": len(cache_files),
                "total_size_bytes": total_size,
                "cache_dir": str(self.cache_dir),
                "cache_hits": self.cache_hits,
                "cache_misses": self.cache_misses,
                "cache_hit_rate": f"{cache_hit_rate:.2%}",
                "avg_request_time_seconds": f"{avg_request_time:.2f}",
                "total_requests": len(self.request_times),
            }
        except Exception:
            return {"error": "Could not get cache stats"}

class HarmonyFormat:
    """Utilities for Harmony format (GPT-OSS chat format)."""

    @staticmethod
    def create_tool_call(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Create a tool call in Harmony format."""
        return {"type": "tool_call", "tool_name": tool_name, "arguments": arguments}

    @staticmethod
    def create_tool_result(tool_name: str, result: Any) -> Dict[str, Any]:
        """Create a tool result in Harmony format."""
        return {"type": "tool_result", "tool_name": tool_name, "result": result}

    @staticmethod
    def format_conversation(messages: List[Dict[str, Any]]) -> str:
        """Format conversation for GPT-OSS."""
        formatted = []
        for msg in messages:
            if msg["role"] == "user":
                formatted.append(f"<|user|>\n{msg['content']}<|end|>")
            elif msg["role"] == "assistant":
                formatted.append(f"<|assistant|>\n{msg['content']}<|end|>")
            elif msg["role"] == "system":
                formatted.append(f"<|system|>\n{msg['content']}<|end|>")
        return "\n".join(formatted)

# Global client instance
gpt_oss_client = GPTOSSClient()
