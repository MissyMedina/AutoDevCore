#!/usr/bin/env python3
"""
Real Integration Test for Collaboration Platform
Tests actual WebSocket server and full collaboration functionality
"""

import asyncio
import json
import time
import threading
import websockets
import uuid
from pathlib import Path
import sys

# Add plugins directory to path
sys.path.append(str(Path(__file__).parent / "plugins"))

from websocket_server import collaboration_manager, run_websocket_server
from team_manager import team_manager, TeamRole, Permission
from collaboration_platform import collaboration_platform


class CollaborationIntegrationTest:
    """Real integration test for collaboration platform."""

    def __init__(self):
        self.websocket_server_thread = None
        self.test_results = {}
        self.websocket_url = "ws://localhost:8765"

    def start_websocket_server(self):
        """Start the WebSocket server in a separate thread."""
        print("🚀 Starting WebSocket server...")
        self.websocket_server_thread = threading.Thread(
            target=run_websocket_server, args=("localhost", 8765), daemon=True
        )
        self.websocket_server_thread.start()

        # Wait for server to start
        time.sleep(3)
        print("✅ WebSocket server started")

    async def test_websocket_connection(self):
        """Test actual WebSocket connection and messaging."""
        print("🔌 Testing WebSocket connection...")

        try:
            # Connect to WebSocket server
            async with websockets.connect(self.websocket_url) as websocket:
                print("✅ Connected to WebSocket server")

                # Test join workspace message
                join_message = {
                    "type": "join_workspace",
                    "workspace_id": "test_workspace_123",
                    "user_id": "test_user_1",
                    "user_name": "Test User 1",
                }

                await websocket.send(json.dumps(join_message))
                print("📤 Sent join workspace message")

                # Wait for response
                response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                response_data = json.loads(response)
                print(f"📥 Received response: {response_data['type']}")

                # Test project update message
                update_message = {
                    "type": "project_update",
                    "workspace_id": "test_workspace_123",
                    "user_id": "test_user_1",
                    "data": {
                        "app_name": "Test Collaborative App",
                        "description": "Testing real-time collaboration",
                        "features": ["Real-time editing", "Team collaboration"],
                    },
                }

                await websocket.send(json.dumps(update_message))
                print("📤 Sent project update message")

                # Wait for broadcast
                broadcast = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                broadcast_data = json.loads(broadcast)
                print(f"📥 Received broadcast: {broadcast_data['type']}")

                return {
                    "success": True,
                    "connection": "established",
                    "messages_sent": 2,
                    "messages_received": 2,
                    "response_types": [
                        response_data.get("type"),
                        broadcast_data.get("type"),
                    ],
                }

        except Exception as e:
            print(f"❌ WebSocket test failed: {e}")
            return {"success": False, "error": str(e)}

    def test_team_management(self):
        """Test real team management functionality."""
        print("👥 Testing team management...")

        try:
            # Create a real team
            team = team_manager.create_team(
                name="Integration Test Team",
                description="Team for integration testing",
                owner_id="test_owner_1",
                owner_email="owner@integration.test",
                is_public=False,
            )
            print(f"✅ Created team: {team.name} (ID: {team.id})")

            # Create invitation
            invitation = team_manager.create_invitation(
                team_id=team.id,
                email="member@integration.test",
                role=TeamRole.EDITOR,
                invited_by="test_owner_1",
            )
            print(f"✅ Created invitation: {invitation.email}")

            # Test permissions
            can_edit = team_manager.has_permission(
                team.id, "test_owner_1", Permission.EDIT_PROJECT
            )
            can_invite = team_manager.has_permission(
                team.id, "test_owner_1", Permission.INVITE_MEMBERS
            )

            print(
                f"✅ Permission test - Owner can edit: {can_edit}, can invite: {can_invite}"
            )

            # Get analytics
            analytics = team_manager.get_team_analytics(team.id, "test_owner_1")
            print(
                f"✅ Analytics: {analytics['total_members']} members, {analytics['activity_rate']}% activity"
            )

            return {
                "success": True,
                "team_id": team.id,
                "team_name": team.name,
                "invitation_id": invitation.id,
                "permissions": {"can_edit": can_edit, "can_invite": can_invite},
                "analytics": analytics,
            }

        except Exception as e:
            print(f"❌ Team management test failed: {e}")
            return {"success": False, "error": str(e)}

    async def test_collaboration_platform(self):
        """Test the full collaboration platform integration."""
        print("🤝 Testing collaboration platform...")

        try:
            # Start the platform
            collaboration_platform.start()
            print("✅ Collaboration platform started")

            # Wait for startup
            await asyncio.sleep(2)

            # Create collaborative project
            project_result = collaboration_platform.create_collaborative_project(
                project_name="Integration Test Project",
                description="Real integration test project",
                owner_id="test_owner_1",
                owner_email="owner@integration.test",
                team_name="Integration Test Team",
            )

            if project_result["success"]:
                print(
                    f"✅ Created collaborative project: {project_result['project_name']}"
                )

                team_id = project_result["team_id"]
                workspace_id = project_result["workspace_id"]

                # Test invitation
                invite_result = collaboration_platform.invite_to_project(
                    team_id=team_id,
                    workspace_id=workspace_id,
                    email="developer@integration.test",
                    role=TeamRole.EDITOR,
                    invited_by="test_owner_1",
                )

                if invite_result["success"]:
                    print(f"✅ Invited team member: {invite_result['email']}")

                # Get project status
                status_result = collaboration_platform.get_project_status(
                    team_id=team_id, workspace_id=workspace_id, user_id="test_owner_1"
                )

                if status_result["success"]:
                    print(f"✅ Project status: {status_result['team']['name']}")

                # Get user dashboard
                dashboard_result = collaboration_platform.get_user_dashboard(
                    "test_owner_1"
                )

                if dashboard_result["success"]:
                    print(f"✅ User dashboard: {len(dashboard_result['teams'])} teams")

                # Stop the platform
                collaboration_platform.stop()
                print("✅ Collaboration platform stopped")

                return {
                    "success": True,
                    "project_creation": project_result,
                    "invitation": invite_result,
                    "project_status": status_result,
                    "user_dashboard": dashboard_result,
                }
            else:
                collaboration_platform.stop()
                return {
                    "success": False,
                    "error": "Failed to create collaborative project",
                }

        except Exception as e:
            print(f"❌ Collaboration platform test failed: {e}")
            collaboration_platform.stop()
            return {"success": False, "error": str(e)}

    async def run_full_integration_test(self):
        """Run the complete integration test."""
        print("🧪 Starting Full Collaboration Integration Test")
        print("=" * 60)

        # Start WebSocket server
        self.start_websocket_server()

        # Test WebSocket connection
        websocket_result = await self.test_websocket_connection()
        self.test_results["websocket"] = websocket_result

        # Test team management
        team_result = self.test_team_management()
        self.test_results["team_management"] = team_result

        # Test collaboration platform
        platform_result = await self.test_collaboration_platform()
        self.test_results["collaboration_platform"] = platform_result

        # Generate summary
        self.generate_test_summary()

        return self.test_results

    def generate_test_summary(self):
        """Generate a comprehensive test summary."""
        print("\n" + "=" * 60)
        print("📊 INTEGRATION TEST SUMMARY")
        print("=" * 60)

        all_passed = True

        for test_name, result in self.test_results.items():
            status = "✅ PASSED" if result.get("success", False) else "❌ FAILED"
            print(f"{test_name.upper()}: {status}")

            if not result.get("success", False):
                all_passed = False
                print(f"   Error: {result.get('error', 'Unknown error')}")

        print("\n" + "=" * 60)
        if all_passed:
            print("🎉 ALL TESTS PASSED! Collaboration platform is fully functional!")
        else:
            print("⚠️  SOME TESTS FAILED. Check errors above.")
        print("=" * 60)


async def main():
    """Main test runner."""
    test = CollaborationIntegrationTest()
    results = await test.run_full_integration_test()

    # Save results to file
    with open("collaboration_integration_test_results.json", "w") as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n📄 Test results saved to: collaboration_integration_test_results.json")

    return results


if __name__ == "__main__":
    asyncio.run(main())
