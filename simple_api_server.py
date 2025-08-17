#!/usr/bin/env python3
"""
Simple API Server for AutoDevCore
A lightweight API server without complex dependencies
"""

import json
import asyncio
from aiohttp import web, ClientSession
import aiohttp_cors


class SimpleAutoDevAPI:
    """Simple API server for AutoDevCore."""

    def __init__(self, host="localhost", port=8080):
        self.host = host
        self.port = port
        self.app = web.Application()
        self.setup_routes()
        self.setup_cors()

    def setup_cors(self):
        """Setup CORS for the application."""
        cors = aiohttp_cors.setup(
            self.app,
            defaults={
                "*": aiohttp_cors.ResourceOptions(
                    allow_credentials=True,
                    expose_headers="*",
                    allow_headers="*",
                    allow_methods="*",
                )
            },
        )

        # Add CORS to all routes
        for route in list(self.app.router.routes()):
            cors.add(route)

    def setup_routes(self):
        """Setup API routes."""
        self.app.router.add_get("/health", self.health_check)
        self.app.router.add_get("/api/status", self.get_status)
        self.app.router.add_post("/auth/login", self.login)
        self.app.router.add_get("/api/user/profile", self.get_profile)
        self.app.router.add_options("/{path:.*}", self.handle_preflight)

    async def health_check(self, request):
        """Health check endpoint."""
        return web.json_response(
            {
                "status": "healthy",
                "service": "AutoDevCore Simple API",
                "version": "1.0.0",
                "port": self.port,
            }
        )

    async def get_status(self, request):
        """Get system status."""
        return web.json_response(
            {
                "status": "running",
                "services": {
                    "api": "active",
                    "gui": "check http://localhost:8501",
                    "websocket": "check ws://localhost:8765",
                },
                "timestamp": asyncio.get_event_loop().time(),
            }
        )

    async def login(self, request):
        """Simple login endpoint."""
        try:
            data = await request.json()
            username = data.get("username")
            password = data.get("password")

            # Simple authentication (for demo)
            if username == "admin" and password == "admin123":
                return web.json_response(
                    {
                        "success": True,
                        "message": "Login successful",
                        "user": {"username": username, "role": "admin"},
                        "token": "demo-jwt-token",
                    }
                )
            else:
                return web.json_response(
                    {"success": False, "error": "Invalid credentials"}, status=401
                )

        except Exception as e:
            return web.json_response(
                {"success": False, "error": f"Login failed: {str(e)}"}, status=500
            )

    async def get_profile(self, request):
        """Get user profile."""
        return web.json_response(
            {
                "user": {
                    "username": "admin",
                    "role": "administrator",
                    "permissions": ["read", "write", "admin"],
                },
                "preferences": {"theme": "dark", "language": "en"},
            }
        )

    async def handle_preflight(self, request):
        """Handle CORS preflight requests."""
        return web.Response(
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization",
            }
        )

    async def start(self):
        """Start the API server."""
        runner = web.AppRunner(self.app)
        await runner.setup()

        site = web.TCPSite(runner, self.host, self.port)
        await site.start()

        print(f"🚀 Simple API Server started at http://{self.host}:{self.port}")
        print(f"📋 Health check: http://{self.host}:{self.port}/health")
        print(f"🔐 Login: POST http://{self.host}:{self.port}/auth/login")
        print(f"📊 Status: http://{self.host}:{self.port}/api/status")

        return runner

    async def stop(self, runner):
        """Stop the API server."""
        await runner.cleanup()


async def main():
    """Main function to run the API server."""
    api = SimpleAutoDevAPI()
    runner = await api.start()

    try:
        # Keep the server running
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping API server...")
        await api.stop(runner)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 API server stopped")
