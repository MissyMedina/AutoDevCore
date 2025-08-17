#!/usr/bin/env python3
"""
AutoDevCore Service Launcher with Port Management
Starts all services with intelligent port detection and fallback
"""

import os
import socket
import subprocess
import sys
import threading
import time
from pathlib import Path


class ServiceLauncher:
    """Manages AutoDevCore service startup with port conflict resolution."""

    def __init__(self):
        self.project_root = Path(__file__).parent
        self.services = {}
        self.default_ports = {"gui": 8501, "api": 8080, "websocket": 8765}
        self.alternative_ports = {
            "gui": [8502, 8503, 8504, 8505],
            "api": [8081, 8082, 8083, 8084],
            "websocket": [8766, 8767, 8768, 8769],
        }

    def check_port(self, port):
        """Check if a port is available."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex(("localhost", port))
                return result != 0  # Port is available if connection fails
        except Exception:
            return False

    def find_available_port(self, service_name):
        """Find an available port for a service."""
        # Try default port first
        default_port = self.default_ports[service_name]
        if self.check_port(default_port):
            return default_port

        # Try alternative ports
        for port in self.alternative_ports[service_name]:
            if self.check_port(port):
                return port

        # If all predefined ports are taken, find any available port
        for port in range(8500, 8600):
            if self.check_port(port):
                return port

        raise Exception(f"No available ports found for {service_name}")

    def start_gui(self, port):
        """Start the Streamlit GUI."""
        print(f"🖥️ Starting GUI on port {port}...")

        gui_path = self.project_root / "gui" / "main.py"
        if not gui_path.exists():
            print(f"❌ GUI file not found: {gui_path}")
            return None

        try:
            # Start Streamlit with custom port
            process = subprocess.Popen(
                [
                    sys.executable,
                    "-m",
                    "streamlit",
                    "run",
                    str(gui_path),
                    "--server.port",
                    str(port),
                    "--server.address",
                    "localhost",
                    "--browser.gatherUsageStats",
                    "false",
                    "--server.headless",
                    "true",
                ],
                cwd=self.project_root,
            )

            # Wait a moment to see if it starts successfully
            time.sleep(3)
            if process.poll() is None:
                print(f"✅ GUI started successfully on http://localhost:{port}")
                return process
            else:
                print(f"❌ GUI failed to start")
                return None

        except Exception as e:
            print(f"❌ Error starting GUI: {e}")
            return None

    def start_api(self, port):
        """Start the REST API server."""
        print(f"🔗 Starting API server on port {port}...")

        # Create a modified API starter script
        api_script = f"""

import sys
import asyncio
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from integrations.web_api import AutoDevCoreAPI

async def main():
    api = AutoDevCoreAPI(host="localhost", port={port})
    runner = await api.start()
    print(f"🚀 API Server running on http://localhost:{port}")
    print(f"📋 Health check: http://localhost:{port}/health")

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await api.stop(runner)

if __name__ == "__main__":
    asyncio.run(main())
"""

        # Write temporary API script
        temp_api_path = self.project_root / "temp_api_server.py"
        with open(temp_api_path, "w") as f:
            f.write(api_script)

        try:
            process = subprocess.Popen(
                [sys.executable, str(temp_api_path)], cwd=self.project_root
            )

            # Wait to see if it starts
            time.sleep(2)
            if process.poll() is None:
                print(f"✅ API server started on http://localhost:{port}")
                return process
            else:
                print(f"❌ API server failed to start")
                return None

        except Exception as e:
            print(f"❌ Error starting API server: {e}")
            return None

    def start_websocket(self, port):
        """Start the WebSocket server."""
        print(f"🔌 Starting WebSocket server on port {port}...")

        # Create WebSocket starter script
        ws_script = f'''

import sys
import asyncio
import websockets
import json
import logging
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

async def handle_connection(websocket, path):
    """Handle WebSocket connections."""
    try:
        print(f"New connection from {{websocket.remote_address}}")

        # Send welcome message
        await websocket.send(json.dumps({{
            "type": "connection_established",
            "message": "Connected to AutoDevCore WebSocket",
            "port": {port}
        }}))

        # Keep connection alive
        async for message in websocket:
            try:
                data = json.loads(message)
                # Echo back the message
                await websocket.send(json.dumps({{
                    "type": "echo",
                    "original": data,
                    "timestamp": str(asyncio.get_event_loop().time())
                }}))
            except json.JSONDecodeError:
                await websocket.send(json.dumps({{
                    "type": "error",
                    "message": "Invalid JSON"
                }}))

    except Exception as e:
        print(f"WebSocket error: {{e}}")

async def main():
    print(f"🔌 Starting WebSocket server on ws://localhost:{port}")

    try:
        server = await websockets.serve(handle_connection, "localhost", {port})
        print(f"✅ WebSocket server running on ws://localhost:{port}")
        await server.wait_closed()
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ Port {port} is already in use")
        else:
            print(f"❌ WebSocket server error: {{e}}")

if __name__ == "__main__":
    asyncio.run(main())
'''

        # Write temporary WebSocket script
        temp_ws_path = self.project_root / "temp_websocket_server.py"
        with open(temp_ws_path, "w") as f:
            f.write(ws_script)

        try:
            process = subprocess.Popen(
                [sys.executable, str(temp_ws_path)], cwd=self.project_root
            )

            # Wait to see if it starts
            time.sleep(2)
            if process.poll() is None:
                print(f"✅ WebSocket server started on ws://localhost:{port}")
                return process
            else:
                print(f"❌ WebSocket server failed to start")
                return None

        except Exception as e:
            print(f"❌ Error starting WebSocket server: {e}")
            return None

    def start_all_services(self):
        """Start all AutoDevCore services."""
        print("🚀 AutoDevCore Service Launcher")
        print("=" * 50)

        # Find available ports
        try:
            gui_port = self.find_available_port("gui")
            api_port = self.find_available_port("api")
            ws_port = self.find_available_port("websocket")

            print(f"📋 Port Assignment:")
            print(f"   GUI: {gui_port}")
            print(f"   API: {api_port}")
            print(f"   WebSocket: {ws_port}")
            print()

        except Exception as e:
            print(f"❌ Port assignment failed: {e}")
            return False

        # Start services
        services_started = []

        # Start API first (other services may depend on it)
        api_process = self.start_api(api_port)
        if api_process:
            self.services["api"] = {"process": api_process, "port": api_port}
            services_started.append("API")

        # Start WebSocket server
        ws_process = self.start_websocket(ws_port)
        if ws_process:
            self.services["websocket"] = {"process": ws_process, "port": ws_port}
            services_started.append("WebSocket")

        # Start GUI last (it's the main interface)
        gui_process = self.start_gui(gui_port)
        if gui_process:
            self.services["gui"] = {"process": gui_process, "port": gui_port}
            services_started.append("GUI")

        # Summary
        print("\n" + "=" * 50)
        print("🎯 SERVICE SUMMARY")
        print("=" * 50)

        if services_started:
            print(
                f"✅ Started {len(services_started)} services: {', '.join(services_started)}"
            )
            print("\n🌐 Access URLs:")

            if "gui" in self.services:
                print(f"   🖥️  GUI: http://localhost:{self.services['gui']['port']}")
            if "api" in self.services:
                print(f"   🔗 API: http://localhost:{self.services['api']['port']}")
                print(
                    f"   💚 Health: http://localhost:{self.services['api']['port']}/health"
                )
            if "websocket" in self.services:
                print(
                    f"   🔌 WebSocket: ws://localhost:{self.services['websocket']['port']}"
                )

            print("\n⏹️  Press Ctrl+C to stop all services")
            return True
        else:
            print("❌ No services started successfully")
            return False

    def stop_all_services(self):
        """Stop all running services."""
        print("\n🛑 Stopping all services...")

        for service_name, service_info in self.services.items():
            try:
                process = service_info["process"]
                if process and process.poll() is None:
                    process.terminate()
                    process.wait(timeout=5)
                    print(f"✅ Stopped {service_name}")
            except Exception as e:
                print(f"❌ Error stopping {service_name}: {e}")

        # Clean up temporary files
        temp_files = ["temp_api_server.py", "temp_websocket_server.py"]
        for temp_file in temp_files:
            temp_path = self.project_root / temp_file
            if temp_path.exists():
                temp_path.unlink()

        print("👋 All services stopped")


def main():
    """Main launcher function."""
    launcher = ServiceLauncher()

    try:
        success = launcher.start_all_services()
        if success:
            # Keep the launcher running
            while True:
                time.sleep(1)
        else:
            print("❌ Failed to start services")
            return 1

    except KeyboardInterrupt:
        launcher.stop_all_services()
    except Exception as e:
        print(f"❌ Launcher error: {e}")
        launcher.stop_all_services()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
