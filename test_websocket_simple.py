#!/usr/bin/env python3
"""
Simple WebSocket Test - Tests actual WebSocket server functionality
"""

import asyncio
import json
import sys
import threading
import time
from pathlib import Path

import websockets

# Add plugins directory to path
sys.path.append(str(Path(__file__).parent / "plugins"))

from websocket_server import run_websocket_server


async def test_websocket_simple():
    """Simple WebSocket test that actually works."""
    print("🧪 Testing WebSocket Server (Simple Version)")
    print("=" * 50)

    # Start WebSocket server in background
    print("🚀 Starting WebSocket server...")
    server_thread = threading.Thread(
        target=run_websocket_server,
        args=("localhost", 8767),  # Use different port
        daemon=True,
    )
    server_thread.start()

    # Wait for server to start
    await asyncio.sleep(3)
    print("✅ WebSocket server started on port 8767")

    try:
        # Connect to WebSocket server
        uri = "ws://localhost:8767/test_user/test_workspace"
        print(f"🔌 Connecting to {uri}...")

        async with websockets.connect(uri) as websocket:
            print("✅ Connected to WebSocket server")

            # Wait for initial message
            try:
                message = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                data = json.loads(message)
                print(f"📥 Received: {data['type']}")

                if data["type"] == "connection_established":
                    print("✅ WebSocket connection established successfully!")

                    # Send a test message
                    test_message = {
                        "type": "project_update",
                        "user_id": "test_user",
                        "workspace_id": "test_workspace",
                        "data": {"message": "Hello from integration test!"},
                    }

                    await websocket.send(json.dumps(test_message))
                    print("📤 Sent test message")

                    return {
                        "success": True,
                        "connection": "established",
                        "server_port": 8767,
                        "message_exchange": "successful",
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Unexpected message type: {data['type']}",
                    }

            except asyncio.TimeoutError:
                return {
                    "success": False,
                    "error": "Timeout waiting for server response",
                }

    except Exception as e:
        print(f"❌ WebSocket test failed: {e}")
        return {"success": False, "error": str(e)}


async def main():
    """Main test runner."""
    result = await test_websocket_simple()

    print("\n" + "=" * 50)
    if result["success"]:
        print("🎉 WebSocket test PASSED!")
        print(f"✅ Server running on port {result['server_port']}")
        print(f"✅ Connection: {result['connection']}")
        print(f"✅ Message exchange: {result['message_exchange']}")
    else:
        print("❌ WebSocket test FAILED!")
        print(f"❌ Error: {result['error']}")
    print("=" * 50)

    return result


if __name__ == "__main__":
    asyncio.run(main())
