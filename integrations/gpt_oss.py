"""
GPT-OSS Integration Module for AutoDevCore

This module provides integration with OpenAI's GPT-OSS models running locally via Ollama.
It handles the Harmony Format for tool interaction and structured reasoning.
"""

import json
import requests
import time
from typing import Dict, List, Optional, Any
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class GPTOSSClient:
    """Client for interacting with GPT-OSS models via Ollama."""
    
    def __init__(self, model_name: str = "gpt-oss:20b", base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url
        self.session = requests.Session()
        
    def _make_request(self, endpoint: str, data: Dict) -> Dict:
        """Make a request to the Ollama API."""
        try:
            # Add optimization parameters for faster inference
            if 'options' not in data:
                data['options'] = {}
            
            # Optimize for speed
            data['options'].update({
                'num_ctx': 2048,  # Smaller context window
                'num_thread': 8,  # Use more threads
                'temperature': 0.3,  # Lower temperature for more focused responses
                'top_p': 0.9,
                'top_k': 40
            })
            
            response = self.session.post(
                f"{self.base_url}{endpoint}",
                json=data,
                timeout=300  # 5 minute timeout for large models
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise
    
    def generate(self, prompt: str, system_message: str = None, 
                tools: List[Dict] = None, temperature: float = 0.3,
                max_tokens: int = 1000) -> Dict:
        """
        Generate a response using GPT-OSS.
        
        Args:
            prompt: The user prompt
            system_message: Optional system message
            tools: List of tool definitions for function calling
            temperature: Sampling temperature (default 0.3 for faster, focused responses)
            max_tokens: Maximum tokens to generate (reduced for speed)
            
        Returns:
            Dict containing the response
        """
        messages = []
        
        if system_message:
            messages.append({"role": "system", "content": system_message})
        
        messages.append({"role": "user", "content": prompt})
        
        request_data = {
            "model": self.model_name,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
                "num_ctx": 2048,  # Smaller context for speed
                "num_thread": 8,  # More threads
                "top_p": 0.9,
                "top_k": 40
            }
        }
        
        if tools:
            request_data["tools"] = tools
        
        return self._make_request("/api/chat", request_data)
    
    def generate_with_tools(self, prompt: str, tools: List[Dict], 
                          system_message: str = None) -> Dict:
        """
        Generate a response with tool calling capabilities.
        
        Args:
            prompt: The user prompt
            tools: List of tool definitions
            system_message: Optional system message
            
        Returns:
            Dict containing the response and any tool calls
        """
        return self.generate(prompt, system_message, tools)
    
    def analyze_code(self, code: str, analysis_type: str = "general") -> str:
        """
        Analyze code using GPT-OSS.
        
        Args:
            code: The code to analyze
            analysis_type: Type of analysis (general, security, performance, etc.)
            
        Returns:
            Analysis result as string
        """
        system_message = f"""You are an expert code analyst. Analyze the provided code for {analysis_type} issues, 
        best practices, and potential improvements. Provide clear, actionable feedback."""
        
        prompt = f"Please analyze this code for {analysis_type} considerations:\n\n```\n{code}\n```"
        
        response = self.generate(prompt, system_message)
        return response.get("message", {}).get("content", "")
    
    def generate_app_plan(self, idea: str) -> Dict:
        """
        Generate an application development plan using GPT-OSS.
        
        Args:
            idea: The app idea description
            
        Returns:
            Dict containing the app plan
        """
        system_message = """You are an expert software architect. Create a detailed development plan for the given app idea.
        Include:
        - Features and functionality
        - Technology stack recommendations
        - Architecture overview
        - Database schema
        - API endpoints
        - UI/UX considerations
        - Deployment strategy
        
        Return your response as a structured JSON object."""
        
        prompt = f"Create a comprehensive development plan for this app idea: {idea}"
        
        response = self.generate(prompt, system_message, temperature=0.3)
        content = response.get("message", {}).get("content", "")
        
        try:
            # Try to extract JSON from the response
            if "```json" in content:
                json_start = content.find("```json") + 7
                json_end = content.find("```", json_start)
                json_str = content[json_start:json_end].strip()
                return json.loads(json_str)
            else:
                # Fallback: try to find JSON in the response
                import re
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
                else:
                    # Return as structured text
                    return {"plan": content}
        except json.JSONDecodeError:
            return {"plan": content}
    
    def generate_code(self, requirements: str, language: str = "python") -> str:
        """
        Generate code based on requirements using GPT-OSS.
        
        Args:
            requirements: Code requirements description
            language: Programming language
            
        Returns:
            Generated code as string
        """
        system_message = f"""You are an expert {language} developer. Generate clean, well-documented code based on the requirements.
        Include proper error handling, comments, and follow best practices."""
        
        prompt = f"Generate {language} code for the following requirements:\n\n{requirements}"
        
        response = self.generate(prompt, system_message, temperature=0.2)
        return response.get("message", {}).get("content", "")
    
    def score_application(self, app_description: str, criteria: Dict) -> Dict:
        """
        Score an application against given criteria using GPT-OSS.
        
        Args:
            app_description: Description of the application
            criteria: Scoring criteria dictionary
            
        Returns:
            Dict containing scores and feedback
        """
        system_message = """You are an expert application evaluator. Score the given application against the provided criteria.
        Provide numerical scores (0-10) for each criterion and detailed feedback explaining your reasoning."""
        
        criteria_text = "\n".join([f"- {k}: {v}" for k, v in criteria.items()])
        prompt = f"""Evaluate this application:

Application: {app_description}

Criteria:
{criteria_text}

Provide scores and detailed feedback for each criterion."""
        
        response = self.generate(prompt, system_message, temperature=0.3)
        return {"evaluation": response.get("message", {}).get("content", "")}

class HarmonyFormat:
    """Utilities for working with GPT-OSS Harmony Format."""
    
    @staticmethod
    def create_tool_call(tool_name: str, arguments: Dict) -> Dict:
        """Create a tool call in Harmony Format."""
        return {
            "type": "tool_call",
            "tool_name": tool_name,
            "arguments": arguments
        }
    
    @staticmethod
    def create_tool_result(tool_name: str, result: Any) -> Dict:
        """Create a tool result in Harmony Format."""
        return {
            "type": "tool_result",
            "tool_name": tool_name,
            "result": result
        }
    
    @staticmethod
    def format_conversation(messages: List[Dict]) -> str:
        """Format conversation history for GPT-OSS."""
        formatted = []
        for msg in messages:
            if msg["role"] == "user":
                formatted.append(f"<|im_start|>user\n{msg['content']}<|im_end|>")
            elif msg["role"] == "assistant":
                formatted.append(f"<|im_start|>assistant\n{msg['content']}<|im_end|>")
            elif msg["role"] == "system":
                formatted.append(f"<|im_start|>system\n{msg['content']}<|im_end|>")
        return "\n".join(formatted)

# Global client instance
gpt_oss_client = GPTOSSClient()
