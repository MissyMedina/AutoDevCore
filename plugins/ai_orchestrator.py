#!/usr/bin/env python3
"""
AI Orchestrator - Integrates multi-model AI with existing agents
"""

import asyncio
import time
from typing import Dict, Any, Optional
from pathlib import Path
import sys

# Add plugins directory to path for imports
sys.path.append(str(Path(__file__).parent.parent / "plugins"))

from multi_model_ai import (
    MultiModelAI, AIRequest, AIResponse, TaskType, 
    ModelProvider, generate_ai_response
)


class AIOrchestrator:
    """Orchestrates AI operations across multiple models and agents."""
    
    def __init__(self):
        self.multi_model_ai = MultiModelAI()
        self.performance_cache = {}
        self.task_mapping = {
            "app_planning": TaskType.APP_PLANNING,
            "code_generation": TaskType.CODE_GENERATION,
            "analysis": TaskType.ANALYSIS,
            "scoring": TaskType.SCORING,
            "documentation": TaskType.DOCUMENTATION
        }
    
    async def generate_response(self, 
                              prompt: str, 
                              task_type: str,
                              priority: str = "normal",
                              **kwargs) -> AIResponse:
        """Generate AI response using optimal model selection."""
        
        # Map task type to enum
        task_enum = self.task_mapping.get(task_type, TaskType.ANALYSIS)
        
        # Create AI request
        request = AIRequest(
            prompt=prompt,
            task_type=task_enum,
            priority=priority,
            **kwargs
        )
        
        # Generate response using multi-model AI
        async with self.multi_model_ai as ai:
            response = await ai.generate(request)
        
        return response
    
    async def generate_app_plan(self, description: str, **kwargs) -> Dict[str, Any]:
        """Generate application plan using optimal AI model."""
        prompt = f"""
Create a comprehensive application plan for: {description}

Provide a JSON response with the following structure:
{{
    "app_name": "string",
    "description": "string",
    "features": ["list", "of", "features"],
    "tech_stack": {{
        "backend": "string",
        "database": "string",
        "frontend": "string"
    }},
    "architecture": "string",
    "database_schema": [],
    "api_endpoints": [],
    "ui_components": [],
    "deployment": "string"
}}
"""
        
        response = await self.generate_response(
            prompt=prompt,
            task_type="app_planning",
            priority="high",
            **kwargs
        )
        
        return {
            "success": response.success,
            "content": response.content,
            "model_used": response.model_used,
            "provider": response.provider.value,
            "response_time": response.response_time,
            "cost": response.cost
        }
    
    async def generate_code(self, 
                          component: str, 
                          requirements: str, 
                          **kwargs) -> Dict[str, Any]:
        """Generate code using optimal AI model."""
        prompt = f"""
Generate {component} code with the following requirements:
{requirements}

Provide clean, well-documented code with proper error handling and security considerations.
"""
        
        response = await self.generate_response(
            prompt=prompt,
            task_type="code_generation",
            priority="normal",
            **kwargs
        )
        
        return {
            "success": response.success,
            "content": response.content,
            "model_used": response.model_used,
            "provider": response.provider.value,
            "response_time": response.response_time,
            "cost": response.cost
        }
    
    async def analyze_code(self, 
                          code: str, 
                          analysis_type: str = "general", 
                          **kwargs) -> Dict[str, Any]:
        """Analyze code using optimal AI model."""
        prompt = f"""
Analyze the following code for {analysis_type}:

{code}

Provide a comprehensive analysis including:
- Code quality assessment
- Security considerations
- Performance implications
- Improvement suggestions
"""
        
        response = await self.generate_response(
            prompt=prompt,
            task_type="analysis",
            priority="normal",
            **kwargs
        )
        
        return {
            "success": response.success,
            "content": response.content,
            "model_used": response.model_used,
            "provider": response.provider.value,
            "response_time": response.response_time,
            "cost": response.cost
        }
    
    async def score_application(self, 
                              app_path: str, 
                              template: str = "general", 
                              **kwargs) -> Dict[str, Any]:
        """Score application using optimal AI model."""
        prompt = f"""
Score the application at {app_path} using the {template} template.

Provide a comprehensive scoring report including:
- Overall score (0-100)
- Category breakdown
- Strengths and weaknesses
- Improvement recommendations
"""
        
        response = await self.generate_response(
            prompt=prompt,
            task_type="scoring",
            priority="normal",
            **kwargs
        )
        
        return {
            "success": response.success,
            "content": response.content,
            "model_used": response.model_used,
            "provider": response.provider.value,
            "response_time": response.response_time,
            "cost": response.cost
        }
    
    async def generate_documentation(self, 
                                   content: str, 
                                   doc_type: str = "readme", 
                                   **kwargs) -> Dict[str, Any]:
        """Generate documentation using optimal AI model."""
        prompt = f"""
Generate {doc_type} documentation for:

{content}

Provide comprehensive, well-structured documentation with examples and usage instructions.
"""
        
        response = await self.generate_response(
            prompt=prompt,
            task_type="documentation",
            priority="low",
            **kwargs
        )
        
        return {
            "success": response.success,
            "content": response.content,
            "model_used": response.model_used,
            "provider": response.provider.value,
            "response_time": response.response_time,
            "cost": response.cost
        }
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get comprehensive performance report."""
        return self.multi_model_ai.get_performance_report()
    
    def get_available_models(self) -> Dict[str, Any]:
        """Get list of available models and their status."""
        report = self.get_performance_report()
        return {
            "model_health": report["model_health"],
            "total_models": report["total_models"],
            "available_models": report["available_models"],
            "task_preferences": report["task_preferences"]
        }
    
    def get_cost_analysis(self) -> Dict[str, Any]:
        """Get cost analysis for AI operations."""
        report = self.get_performance_report()
        performance = report["model_performance"]
        
        total_cost = 0.0
        total_requests = 0
        cost_by_provider = {}
        
        for key, data in performance.items():
            provider = key.split("_")[0]
            requests = data.get("total_requests", 0)
            total_requests += requests
            
            # Estimate cost (this would need to be tracked in actual usage)
            if provider == "openai":
                cost = requests * 0.03  # Approximate cost per request
            elif provider == "anthropic":
                cost = requests * 0.015  # Approximate cost per request
            else:
                cost = 0.0  # GPT-OSS and fallback are free
            
            total_cost += cost
            cost_by_provider[provider] = cost
        
        return {
            "total_cost": total_cost,
            "total_requests": total_requests,
            "cost_by_provider": cost_by_provider,
            "avg_cost_per_request": total_cost / total_requests if total_requests > 0 else 0
        }


# Global orchestrator instance
ai_orchestrator = AIOrchestrator()


# Convenience functions for backward compatibility
async def generate_app_plan(description: str, **kwargs) -> Dict[str, Any]:
    """Generate application plan."""
    return await ai_orchestrator.generate_app_plan(description, **kwargs)


async def generate_code(component: str, requirements: str, **kwargs) -> Dict[str, Any]:
    """Generate code."""
    return await ai_orchestrator.generate_code(component, requirements, **kwargs)


async def analyze_code(code: str, analysis_type: str = "general", **kwargs) -> Dict[str, Any]:
    """Analyze code."""
    return await ai_orchestrator.analyze_code(code, analysis_type, **kwargs)


async def score_application(app_path: str, template: str = "general", **kwargs) -> Dict[str, Any]:
    """Score application."""
    return await ai_orchestrator.score_application(app_path, template, **kwargs)


async def generate_documentation(content: str, doc_type: str = "readme", **kwargs) -> Dict[str, Any]:
    """Generate documentation."""
    return await ai_orchestrator.generate_documentation(content, doc_type, **kwargs)


def run(context=None):
    """Plugin entry point for testing the AI orchestrator."""
    async def test_orchestrator():
        # Test app plan generation
        app_plan_result = await generate_app_plan(
            "A task management application with user authentication"
        )
        
        # Test code generation
        code_result = await generate_code(
            "user authentication",
            "JWT-based authentication with password hashing"
        )
        
        # Test analysis
        analysis_result = await analyze_code(
            "def hello(): print('Hello, World!')",
            "security"
        )
        
        return {
            "status": "success",
            "message": "AI Orchestrator test completed",
            "data": {
                "app_plan": {
                    "success": app_plan_result["success"],
                    "model_used": app_plan_result["model_used"],
                    "response_time": app_plan_result["response_time"]
                },
                "code_generation": {
                    "success": code_result["success"],
                    "model_used": code_result["model_used"],
                    "response_time": code_result["response_time"]
                },
                "analysis": {
                    "success": analysis_result["success"],
                    "model_used": analysis_result["model_used"],
                    "response_time": analysis_result["response_time"]
                },
                "performance_report": ai_orchestrator.get_performance_report(),
                "available_models": ai_orchestrator.get_available_models(),
                "cost_analysis": ai_orchestrator.get_cost_analysis()
            }
        }
    
    # Run the async test
    return asyncio.run(test_orchestrator())
