#!/usr/bin/env python3
"""
Collaboration Package - Real-time team collaboration features
"""

from .collaboration_platform import CollaborationPlatform
from .team_manager import Permission, TeamRole, team_manager
from .websocket_server import collaboration_manager, run_websocket_server

__all__ = [
    "CollaborationPlatform",
    "team_manager",
    "TeamRole",
    "Permission",
    "collaboration_manager",
    "run_websocket_server",
]

# Version info
__version__ = "1.0.0"
__author__ = "AutoDevCore Team"
__description__ = "Real-time collaboration platform for AutoDevCore"
