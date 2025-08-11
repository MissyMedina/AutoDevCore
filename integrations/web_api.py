#!/usr/bin/env python3
"""
AutoDevCore Web API Component
Demonstrates JWT authentication and CORS configuration
"""

import asyncio
import aiohttp
from aiohttp import web
import json
from typing import Dict, Any, Optional
from integrations.jwt_auth import jwt_auth
from integrations.cors_config import cors_manager

class AutoDevCoreAPI:
    """Simple Web API for AutoDevCore with JWT and CORS"""
    
    def __init__(self, host: str = "localhost", port: int = 8080):
        self.host = host
        self.port = port
        self.app = web.Application()
        self.setup_routes()
        self.setup_middleware()
    
    def setup_middleware(self):
        """Setup CORS middleware"""
        @self.app.middleware
        async def cors_middleware(request, handler):
            # Handle preflight requests
            if request.method == 'OPTIONS':
                response = web.Response()
                cors_manager.middleware.add_cors_headers(
                    response.headers,
                    request.headers.get('Origin')
                )
                return response
            
            # Handle regular requests
            response = await handler(request)
            cors_manager.middleware.add_cors_headers(
                response.headers,
                request.headers.get('Origin')
            )
            return response
    
    def setup_routes(self):
        """Setup API routes"""
        # Health check
        self.app.router.add_get('/health', self.health_check)
        
        # Authentication routes
        self.app.router.add_post('/auth/login', self.login)
        self.app.router.add_post('/auth/register', self.register)
        self.app.router.add_post('/auth/refresh', self.refresh_token)
        
        # Protected routes
        self.app.router.add_get('/api/user/profile', self.get_profile)
        self.app.router.add_get('/api/status', self.get_status)
        
        # CORS preflight
        self.app.router.add_route('OPTIONS', '/{path:.*}', self.handle_preflight)
    
    async def health_check(self, request):
        """Health check endpoint"""
        return web.json_response({
            'status': 'healthy',
            'service': 'AutoDevCore API',
            'version': '1.0.0'
        })
    
    async def login(self, request):
        """Login endpoint"""
        try:
            data = await request.json()
            username = data.get('username')
            password = data.get('password')
            
            if not username or not password:
                return web.json_response(
                    {'error': 'Username and password required'},
                    status=400
                )
            
            result = jwt_auth.login(username, password)
            if result:
                return web.json_response({
                    'access_token': result['access_token'],
                    'refresh_token': result['refresh_token'],
                    'user_info': result['user_info']
                })
            else:
                return web.json_response(
                    {'error': 'Invalid credentials'},
                    status=401
                )
        except Exception as e:
            return web.json_response(
                {'error': f'Login failed: {str(e)}'},
                status=500
            )
    
    async def register(self, request):
        """Register endpoint"""
        try:
            data = await request.json()
            username = data.get('username')
            password = data.get('password')
            email = data.get('email')
            
            if not all([username, password, email]):
                return web.json_response(
                    {'error': 'Username, password, and email required'},
                    status=400
                )
            
            success = jwt_auth.create_user(username, password, email)
            if success:
                return web.json_response({
                    'message': 'User created successfully',
                    'username': username
                })
            else:
                return web.json_response(
                    {'error': 'Username already exists'},
                    status=409
                )
        except Exception as e:
            return web.json_response(
                {'error': f'Registration failed: {str(e)}'},
                status=500
            )
    
    async def refresh_token(self, request):
        """Refresh token endpoint"""
        try:
            data = await request.json()
            refresh_token = data.get('refresh_token')
            
            if not refresh_token:
                return web.json_response(
                    {'error': 'Refresh token required'},
                    status=400
                )
            
            new_access_token = jwt_auth.refresh_token(refresh_token)
            if new_access_token:
                return web.json_response({
                    'access_token': new_access_token
                })
            else:
                return web.json_response(
                    {'error': 'Invalid refresh token'},
                    status=401
                )
        except Exception as e:
            return web.json_response(
                {'error': f'Token refresh failed: {str(e)}'},
                status=500
            )
    
    async def get_profile(self, request):
        """Get user profile (protected endpoint)"""
        try:
            # Extract token from Authorization header
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return web.json_response(
                    {'error': 'Authorization header required'},
                    status=401
                )
            
            token = auth_header.split(' ')[1]
            user_info = jwt_auth.get_user_info(token)
            
            if user_info:
                return web.json_response({
                    'profile': user_info
                })
            else:
                return web.json_response(
                    {'error': 'Invalid token'},
                    status=401
                )
        except Exception as e:
            return web.json_response(
                {'error': f'Profile retrieval failed: {str(e)}'},
                status=500
            )
    
    async def get_status(self, request):
        """Get API status (protected endpoint)"""
        try:
            # Extract token from Authorization header
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return web.json_response(
                    {'error': 'Authorization header required'},
                    status=401
                )
            
            token = auth_header.split(' ')[1]
            user_info = jwt_auth.get_user_info(token)
            
            if user_info:
                return web.json_response({
                    'status': 'authenticated',
                    'user': user_info['username'],
                    'role': user_info['role'],
                    'api_version': '1.0.0'
                })
            else:
                return web.json_response(
                    {'error': 'Invalid token'},
                    status=401
                )
        except Exception as e:
            return web.json_response(
                {'error': f'Status retrieval failed: {str(e)}'},
                status=500
            )
    
    async def handle_preflight(self, request):
        """Handle CORS preflight requests"""
        origin = request.headers.get('Origin')
        method = request.headers.get('Access-Control-Request-Method')
        headers = request.headers.get('Access-Control-Request-Headers', '').split(',')
        
        result = cors_manager.middleware.handle_preflight(method, headers)
        
        response = web.Response(status=result['status'], text=result['body'])
        for key, value in result['headers'].items():
            response.headers[key] = value
        
        return response
    
    async def start(self):
        """Start the API server"""
        # Create default admin user if no users exist
        jwt_auth.create_default_admin()
        
        # Create secure CORS configuration
        secure_config = cors_manager.create_secure_config()
        cors_manager.update_config(**secure_config.__dict__)
        
        runner = web.AppRunner(self.app)
        await runner.setup()
        
        site = web.TCPSite(runner, self.host, self.port)
        await site.start()
        
        print(f"🚀 AutoDevCore API started at http://{self.host}:{self.port}")
        print(f"📋 Health check: http://{self.host}:{self.port}/health")
        print(f"🔐 Default admin: admin/admin123")
        
        return runner
    
    async def stop(self, runner):
        """Stop the API server"""
        await runner.cleanup()

# Global API instance
api = AutoDevCoreAPI()

async def start_api_server():
    """Start the API server"""
    runner = await api.start()
    try:
        # Keep the server running
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await api.stop(runner)

if __name__ == "__main__":
    asyncio.run(start_api_server())
