#!/usr/bin/env python3
"""
AutoDevCore Multi-Provider AI Integration
Supports OpenAI, Anthropic, Google AI, Cohere, Mistral, and Perplexity
"""

import json
import requests
import asyncio
import aiohttp
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
import time
import logging

class MultiProviderAI:
    """Multi-provider AI integration with intelligent model selection"""
    
    def __init__(self, config_file: str = "config/api_config.json"):
        self.config_file = Path(config_file)
        self.config = self.load_config()
        self.session = None
        self.logger = logging.getLogger(__name__)
        
        # Provider configurations
        self.providers = {
            'openai': {
                'name': 'OpenAI',
                'base_url': 'https://api.openai.com/v1',
                'headers_template': lambda api_key: {
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json'
                },
                'chat_endpoint': '/chat/completions',
                'models_endpoint': '/models'
            },
            'anthropic': {
                'name': 'Anthropic',
                'base_url': 'https://api.anthropic.com',
                'headers_template': lambda api_key: {
                    'x-api-key': api_key,
                    'Content-Type': 'application/json',
                    'anthropic-version': '2023-06-01'
                },
                'chat_endpoint': '/v1/messages',
                'models_endpoint': '/v1/models'
            },
            'google': {
                'name': 'Google AI',
                'base_url': 'https://generativelanguage.googleapis.com',
                'headers_template': lambda api_key: {
                    'Content-Type': 'application/json'
                },
                'chat_endpoint': '/v1beta/models/{model}:generateContent',
                'models_endpoint': '/v1beta/models'
            },
            'cohere': {
                'name': 'Cohere',
                'base_url': 'https://api.cohere.ai',
                'headers_template': lambda api_key: {
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json'
                },
                'chat_endpoint': '/v1/chat',
                'models_endpoint': '/v1/models'
            },
            'mistral': {
                'name': 'Mistral AI',
                'base_url': 'https://api.mistral.ai',
                'headers_template': lambda api_key: {
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json'
                },
                'chat_endpoint': '/v1/chat/completions',
                'models_endpoint': '/v1/models'
            },
            'perplexity': {
                'name': 'Perplexity',
                'base_url': 'https://api.perplexity.ai',
                'headers_template': lambda api_key: {
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json'
                },
                'chat_endpoint': '/chat/completions',
                'models_endpoint': '/models'
            }
        }
    
    def load_config(self) -> Dict[str, Any]:
        """Load API configuration"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.warning(f"Error loading config: {e}")
                return {}
        return {}
    
    def get_available_providers(self) -> List[str]:
        """Get list of configured providers"""
        return [provider for provider in self.providers.keys() 
                if provider in self.config and self.config[provider].get('api_key')]
    
    def get_provider_config(self, provider: str) -> Optional[Dict[str, Any]]:
        """Get configuration for a specific provider"""
        return self.config.get(provider)
    
    def test_provider_connection(self, provider: str) -> Dict[str, Any]:
        """Test connection to a specific provider"""
        if provider not in self.providers:
            return {'success': False, 'message': f"Unknown provider: {provider}"}
        
        provider_config = self.get_provider_config(provider)
        if not provider_config or not provider_config.get('api_key'):
            return {'success': False, 'message': f"No API key configured for {provider}"}
        
        try:
            provider_info = self.providers[provider]
            headers = provider_info['headers_template'](provider_config['api_key'])
            
            # Test models endpoint
            if provider == 'google':
                params = {'key': provider_config['api_key']}
                response = requests.get(
                    f"{provider_info['base_url']}{provider_info['models_endpoint']}",
                    headers=headers,
                    params=params,
                    timeout=10
                )
            else:
                response = requests.get(
                    f"{provider_info['base_url']}{provider_info['models_endpoint']}",
                    headers=headers,
                    timeout=10
                )
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'message': f"✅ {provider_info['name']} connection successful",
                    'status_code': response.status_code
                }
            else:
                return {
                    'success': False,
                    'message': f"❌ {provider_info['name']} connection failed: {response.status_code}",
                    'status_code': response.status_code
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f"❌ {provider_info['name']} connection error: {str(e)}",
                'status_code': 500
            }
    
    def select_optimal_provider(self, task_type: str = 'general', 
                              complexity: str = 'medium',
                              cost_preference: str = 'balanced') -> Optional[str]:
        """Select the optimal provider based on task and preferences"""
        available_providers = self.get_available_providers()
        
        if not available_providers:
            return None
        
        # Provider rankings based on different criteria
        provider_rankings = {
            'performance': ['openai', 'anthropic', 'google', 'mistral', 'cohere', 'perplexity'],
            'cost': ['perplexity', 'cohere', 'mistral', 'google', 'anthropic', 'openai'],
            'speed': ['google', 'mistral', 'cohere', 'perplexity', 'anthropic', 'openai']
        }
        
        # Task-specific preferences
        task_preferences = {
            'code_generation': ['openai', 'anthropic', 'google'],
            'analysis': ['anthropic', 'openai', 'google'],
            'creative': ['openai', 'anthropic', 'cohere'],
            'research': ['perplexity', 'anthropic', 'openai'],
            'general': ['openai', 'anthropic', 'google']
        }
        
        # Select ranking based on cost preference
        if cost_preference == 'cost_optimized':
            ranking = provider_rankings['cost']
        elif cost_preference == 'performance_optimized':
            ranking = provider_rankings['performance']
        else:  # balanced
            ranking = provider_rankings['performance']
        
        # Filter by task preference
        task_ranking = task_preferences.get(task_type, task_preferences['general'])
        
        # Find the best available provider
        for provider in task_ranking:
            if provider in available_providers:
                return provider
        
        # Fallback to any available provider
        return available_providers[0] if available_providers else None
    
    def format_message_for_provider(self, provider: str, messages: List[Dict[str, str]], 
                                  model: str, **kwargs) -> Dict[str, Any]:
        """Format messages for specific provider API"""
        provider_config = self.get_provider_config(provider)
        if not provider_config:
            raise ValueError(f"No configuration found for provider: {provider}")
        
        if provider == 'openai':
            return {
                'model': model,
                'messages': messages,
                'max_tokens': kwargs.get('max_tokens', provider_config.get('max_tokens', 4000)),
                'temperature': kwargs.get('temperature', provider_config.get('temperature', 0.7)),
                'stream': kwargs.get('stream', False)
            }
        
        elif provider == 'anthropic':
            # Anthropic uses a different message format
            anthropic_messages = []
            for msg in messages:
                if msg['role'] == 'user':
                    anthropic_messages.append({'role': 'user', 'content': msg['content']})
                elif msg['role'] == 'assistant':
                    anthropic_messages.append({'role': 'assistant', 'content': msg['content']})
                elif msg['role'] == 'system':
                    # Anthropic doesn't support system messages in the same way
                    anthropic_messages.append({'role': 'user', 'content': f"System: {msg['content']}"})
            
            return {
                'model': model,
                'messages': anthropic_messages,
                'max_tokens': kwargs.get('max_tokens', provider_config.get('max_tokens', 4000)),
                'temperature': kwargs.get('temperature', provider_config.get('temperature', 0.7))
            }
        
        elif provider == 'google':
            # Google AI uses a different format
            google_messages = []
            for msg in messages:
                google_messages.append({
                    'role': msg['role'],
                    'parts': [{'text': msg['content']}]
                })
            
            return {
                'contents': google_messages,
                'generationConfig': {
                    'maxOutputTokens': kwargs.get('max_tokens', provider_config.get('max_tokens', 4000)),
                    'temperature': kwargs.get('temperature', provider_config.get('temperature', 0.7))
                }
            }
        
        elif provider == 'cohere':
            return {
                'model': model,
                'message': messages[-1]['content'] if messages else '',
                'chat_history': messages[:-1] if len(messages) > 1 else [],
                'max_tokens': kwargs.get('max_tokens', provider_config.get('max_tokens', 4000)),
                'temperature': kwargs.get('temperature', provider_config.get('temperature', 0.7))
            }
        
        elif provider == 'mistral':
            return {
                'model': model,
                'messages': messages,
                'max_tokens': kwargs.get('max_tokens', provider_config.get('max_tokens', 4000)),
                'temperature': kwargs.get('temperature', provider_config.get('temperature', 0.7)),
                'stream': kwargs.get('stream', False)
            }
        
        elif provider == 'perplexity':
            return {
                'model': model,
                'messages': messages,
                'max_tokens': kwargs.get('max_tokens', provider_config.get('max_tokens', 4000)),
                'temperature': kwargs.get('temperature', provider_config.get('temperature', 0.7))
            }
        
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    def parse_provider_response(self, provider: str, response: Dict[str, Any]) -> str:
        """Parse response from specific provider"""
        try:
            if provider == 'openai':
                return response['choices'][0]['message']['content']
            
            elif provider == 'anthropic':
                return response['content'][0]['text']
            
            elif provider == 'google':
                return response['candidates'][0]['content']['parts'][0]['text']
            
            elif provider == 'cohere':
                return response['text']
            
            elif provider == 'mistral':
                return response['choices'][0]['message']['content']
            
            elif provider == 'perplexity':
                return response['choices'][0]['message']['content']
            
            else:
                raise ValueError(f"Unsupported provider: {provider}")
                
        except (KeyError, IndexError) as e:
            self.logger.error(f"Error parsing {provider} response: {e}")
            return f"Error parsing response from {provider}: {str(e)}"
    
    async def generate_response_async(self, prompt: str, 
                                    provider: Optional[str] = None,
                                    model: Optional[str] = None,
                                    task_type: str = 'general',
                                    **kwargs) -> Dict[str, Any]:
        """Generate response asynchronously"""
        start_time = time.time()
        
        # Select provider if not specified
        if not provider:
            provider = self.select_optimal_provider(task_type, **kwargs)
            if not provider:
                return {
                    'success': False,
                    'error': 'No configured providers available',
                    'provider': None
                }
        
        # Get provider configuration
        provider_config = self.get_provider_config(provider)
        if not provider_config:
            return {
                'success': False,
                'error': f'No configuration found for provider: {provider}',
                'provider': provider
            }
        
        # Use default model if not specified
        if not model:
            model = provider_config.get('default_model')
        
        try:
            # Format messages
            messages = [{'role': 'user', 'content': prompt}]
            payload = self.format_message_for_provider(provider, messages, model, **kwargs)
            
            # Prepare request
            provider_info = self.providers[provider]
            headers = provider_info['headers_template'](provider_config['api_key'])
            
            # Make request
            if provider == 'google':
                url = f"{provider_info['base_url']}{provider_info['chat_endpoint'].format(model=model)}"
                params = {'key': provider_config['api_key']}
                async with aiohttp.ClientSession() as session:
                    async with session.post(url, json=payload, params=params, headers=headers) as response:
                        response_data = await response.json()
            else:
                url = f"{provider_info['base_url']}{provider_info['chat_endpoint']}"
                async with aiohttp.ClientSession() as session:
                    async with session.post(url, json=payload, headers=headers) as response:
                        response_data = await response.json()
            
            # Parse response
            if response.status == 200:
                content = self.parse_provider_response(provider, response_data)
                end_time = time.time()
                
                return {
                    'success': True,
                    'content': content,
                    'provider': provider,
                    'model': model,
                    'response_time': end_time - start_time,
                    'raw_response': response_data
                }
            else:
                return {
                    'success': False,
                    'error': f'API request failed: {response.status} - {response_data}',
                    'provider': provider,
                    'response_time': time.time() - start_time
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Request error: {str(e)}',
                'provider': provider,
                'response_time': time.time() - start_time
            }
    
    def generate_response(self, prompt: str, 
                         provider: Optional[str] = None,
                         model: Optional[str] = None,
                         task_type: str = 'general',
                         **kwargs) -> Dict[str, Any]:
        """Generate response synchronously"""
        return asyncio.run(self.generate_response_async(prompt, provider, model, task_type, **kwargs))
    
    def get_provider_status(self) -> Dict[str, Any]:
        """Get status of all configured providers"""
        status = {}
        for provider in self.providers.keys():
            if provider in self.config and self.config[provider].get('api_key'):
                test_result = self.test_provider_connection(provider)
                status[provider] = {
                    'configured': True,
                    'connected': test_result['success'],
                    'message': test_result['message'],
                    'last_updated': self.config[provider].get('last_updated')
                }
            else:
                status[provider] = {
                    'configured': False,
                    'connected': False,
                    'message': 'Not configured',
                    'last_updated': None
                }
        return status
    
    def get_usage_summary(self) -> Dict[str, Any]:
        """Get usage summary for all providers"""
        return self.config.get('usage', {})

# Global instance
multi_provider_ai = MultiProviderAI()
