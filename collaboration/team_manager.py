#!/usr/bin/env python3
"""
Team Manager - Role-based access control and team management
"""

import json
import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set


class Permission(Enum):
    """Available permissions for team members."""

    VIEW_PROJECT = "view_project"
    EDIT_PROJECT = "edit_project"
    DELETE_PROJECT = "delete_project"
    INVITE_MEMBERS = "invite_members"
    REMOVE_MEMBERS = "remove_members"
    MANAGE_ROLES = "manage_roles"
    VIEW_ANALYTICS = "view_analytics"
    MANAGE_SETTINGS = "manage_settings"
    GENERATE_AI = "generate_ai"
    EXPORT_PROJECT = "export_project"


class TeamRole(Enum):
    """Team roles with associated permissions."""

    OWNER = "owner"
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"
    GUEST = "guest"


@dataclass
class TeamMember:
    """Team member information."""

    user_id: str
    username: str
    email: str
    role: TeamRole
    joined_at: datetime
    last_active: datetime
    permissions: Set[Permission] = field(default_factory=set)
    avatar_url: Optional[str] = None
    is_active: bool = True


@dataclass
class Team:
    """Team information."""

    id: str
    name: str
    description: str
    owner_id: str
    created_at: datetime
    updated_at: datetime
    members: Dict[str, TeamMember] = field(default_factory=dict)
    settings: Dict[str, Any] = field(default_factory=dict)
    is_public: bool = False
    max_members: int = 50


@dataclass
class TeamInvitation:
    """Team invitation."""

    id: str
    team_id: str
    email: str
    role: TeamRole
    invited_by: str
    invited_at: datetime
    expires_at: datetime
    is_accepted: bool = False
    accepted_at: Optional[datetime] = None


class TeamManager:
    """Manages teams, members, and permissions."""

    def __init__(self, data_dir: str = "data/teams"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.teams: Dict[str, Team] = {}
        self.invitations: Dict[str, TeamInvitation] = {}
        self.role_permissions: Dict[TeamRole, Set[Permission]] = (
            self._setup_role_permissions()
        )

        self._load_data()

    def _setup_role_permissions(self) -> Dict[TeamRole, Set[Permission]]:
        """Setup default permissions for each role."""
        return {
            TeamRole.OWNER: {
                Permission.VIEW_PROJECT,
                Permission.EDIT_PROJECT,
                Permission.DELETE_PROJECT,
                Permission.INVITE_MEMBERS,
                Permission.REMOVE_MEMBERS,
                Permission.MANAGE_ROLES,
                Permission.VIEW_ANALYTICS,
                Permission.MANAGE_SETTINGS,
                Permission.GENERATE_AI,
                Permission.EXPORT_PROJECT,
            },
            TeamRole.ADMIN: {
                Permission.VIEW_PROJECT,
                Permission.EDIT_PROJECT,
                Permission.INVITE_MEMBERS,
                Permission.REMOVE_MEMBERS,
                Permission.MANAGE_ROLES,
                Permission.VIEW_ANALYTICS,
                Permission.MANAGE_SETTINGS,
                Permission.GENERATE_AI,
                Permission.EXPORT_PROJECT,
            },
            TeamRole.EDITOR: {
                Permission.VIEW_PROJECT,
                Permission.EDIT_PROJECT,
                Permission.GENERATE_AI,
                Permission.EXPORT_PROJECT,
            },
            TeamRole.VIEWER: {Permission.VIEW_PROJECT, Permission.EXPORT_PROJECT},
            TeamRole.GUEST: {Permission.VIEW_PROJECT},
        }

    def _load_data(self):
        """Load teams and invitations from disk."""
        try:
            # Load teams
            teams_file = self.data_dir / "teams.json"
            if teams_file.exists():
                with open(teams_file, "r") as f:
                    teams_data = json.load(f)
                    for team_data in teams_data.values():
                        team = self._deserialize_team(team_data)
                        self.teams[team.id] = team

            # Load invitations
            invitations_file = self.data_dir / "invitations.json"
            if invitations_file.exists():
                with open(invitations_file, "r") as f:
                    invitations_data = json.load(f)
                    for invitation_data in invitations_data.values():
                        invitation = self._deserialize_invitation(invitation_data)
                        self.invitations[invitation.id] = invitation

            logging.info(
                f"Loaded {len(self.teams)} teams and {len(self.invitations)} invitations"
            )
        except Exception as e:
            logging.error(f"Error loading team data: {e}")

    def _save_data(self):
        """Save teams and invitations to disk."""
        try:
            # Save teams
            teams_file = self.data_dir / "teams.json"
            teams_data = {
                team_id: self._serialize_team(team)
                for team_id, team in self.teams.items()
            }
            with open(teams_file, "w") as f:
                json.dump(teams_data, f, indent=2)

            # Save invitations
            invitations_file = self.data_dir / "invitations.json"
            invitations_data = {
                invitation_id: self._serialize_invitation(invitation)
                for invitation_id, invitation in self.invitations.items()
            }
            with open(invitations_file, "w") as f:
                json.dump(invitations_data, f, indent=2)

            logging.info(
                f"Saved {len(self.teams)} teams and {len(self.invitations)} invitations"
            )
        except Exception as e:
            logging.error(f"Error saving team data: {e}")

    def _serialize_team(self, team: Team) -> Dict[str, Any]:
        """Serialize team to dictionary."""
        return {
            "id": team.id,
            "name": team.name,
            "description": team.description,
            "owner_id": team.owner_id,
            "created_at": team.created_at.isoformat(),
            "updated_at": team.updated_at.isoformat(),
            "members": {
                user_id: {
                    "user_id": member.user_id,
                    "username": member.username,
                    "email": member.email,
                    "role": member.role.value,
                    "joined_at": member.joined_at.isoformat(),
                    "last_active": member.last_active.isoformat(),
                    "permissions": [p.value for p in member.permissions],
                    "avatar_url": member.avatar_url,
                    "is_active": member.is_active,
                }
                for user_id, member in team.members.items()
            },
            "settings": team.settings,
            "is_public": team.is_public,
            "max_members": team.max_members,
        }

    def _deserialize_team(self, data: Dict[str, Any]) -> Team:
        """Deserialize team from dictionary."""
        team = Team(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            owner_id=data["owner_id"],
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            settings=data.get("settings", {}),
            is_public=data.get("is_public", False),
            max_members=data.get("max_members", 50),
        )

        # Deserialize members
        for user_id, member_data in data.get("members", {}).items():
            member = TeamMember(
                user_id=member_data["user_id"],
                username=member_data["username"],
                email=member_data["email"],
                role=TeamRole(member_data["role"]),
                joined_at=datetime.fromisoformat(member_data["joined_at"]),
                last_active=datetime.fromisoformat(member_data["last_active"]),
                permissions={Permission(p) for p in member_data.get("permissions", [])},
                avatar_url=member_data.get("avatar_url"),
                is_active=member_data.get("is_active", True),
            )
            team.members[user_id] = member

        return team

    def _serialize_invitation(self, invitation: TeamInvitation) -> Dict[str, Any]:
        """Serialize invitation to dictionary."""
        return {
            "id": invitation.id,
            "team_id": invitation.team_id,
            "email": invitation.email,
            "role": invitation.role.value,
            "invited_by": invitation.invited_by,
            "invited_at": invitation.invited_at.isoformat(),
            "expires_at": invitation.expires_at.isoformat(),
            "is_accepted": invitation.is_accepted,
            "accepted_at": (
                invitation.accepted_at.isoformat() if invitation.accepted_at else None
            ),
        }

    def _deserialize_invitation(self, data: Dict[str, Any]) -> TeamInvitation:
        """Deserialize invitation from dictionary."""
        return TeamInvitation(
            id=data["id"],
            team_id=data["team_id"],
            email=data["email"],
            role=TeamRole(data["role"]),
            invited_by=data["invited_by"],
            invited_at=datetime.fromisoformat(data["invited_at"]),
            expires_at=datetime.fromisoformat(data["expires_at"]),
            is_accepted=data.get("is_accepted", False),
            accepted_at=(
                datetime.fromisoformat(data["accepted_at"])
                if data.get("accepted_at")
                else None
            ),
        )

    def create_team(
        self,
        name: str,
        description: str,
        owner_id: str,
        owner_email: str,
        is_public: bool = False,
    ) -> Team:
        """Create a new team."""
        team_id = str(uuid.uuid4())
        team = Team(
            id=team_id,
            name=name,
            description=description,
            owner_id=owner_id,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            is_public=is_public,
        )

        # Add owner as first member
        owner_member = TeamMember(
            user_id=owner_id,
            username=f"User_{owner_id[:8]}",
            email=owner_email,
            role=TeamRole.OWNER,
            joined_at=datetime.now(),
            last_active=datetime.now(),
            permissions=self.role_permissions[TeamRole.OWNER],
        )
        team.members[owner_id] = owner_member

        self.teams[team_id] = team
        self._save_data()

        logging.info(f"Created team {team_id} by user {owner_id}")
        return team

    def get_team(self, team_id: str) -> Optional[Team]:
        """Get team by ID."""
        return self.teams.get(team_id)

    def get_user_teams(self, user_id: str) -> List[Team]:
        """Get all teams for a user."""
        return [team for team in self.teams.values() if user_id in team.members]

    def add_member(
        self,
        team_id: str,
        user_id: str,
        username: str,
        email: str,
        role: TeamRole,
        added_by: str,
    ) -> bool:
        """Add a member to a team."""
        if team_id not in self.teams:
            return False

        team = self.teams[team_id]

        # Check if user has permission to add members
        if not self.has_permission(team_id, added_by, Permission.INVITE_MEMBERS):
            return False

        # Check if team is full
        if len(team.members) >= team.max_members:
            return False

        # Add member
        member = TeamMember(
            user_id=user_id,
            username=username,
            email=email,
            role=role,
            joined_at=datetime.now(),
            last_active=datetime.now(),
            permissions=self.role_permissions[role],
        )
        team.members[user_id] = member
        team.updated_at = datetime.now()

        self._save_data()
        logging.info(f"Added member {user_id} to team {team_id} with role {role.value}")
        return True

    def remove_member(self, team_id: str, user_id: str, removed_by: str) -> bool:
        """Remove a member from a team."""
        if team_id not in self.teams:
            return False

        team = self.teams[team_id]

        # Check if user has permission to remove members
        if not self.has_permission(team_id, removed_by, Permission.REMOVE_MEMBERS):
            return False

        # Can't remove the owner
        if user_id == team.owner_id:
            return False

        # Can't remove yourself if you're the owner
        if user_id == removed_by and removed_by == team.owner_id:
            return False

        if user_id in team.members:
            del team.members[user_id]
            team.updated_at = datetime.now()
            self._save_data()

            logging.info(f"Removed member {user_id} from team {team_id}")
            return True

        return False

    def update_member_role(
        self, team_id: str, user_id: str, new_role: TeamRole, updated_by: str
    ) -> bool:
        """Update a member's role."""
        if team_id not in self.teams:
            return False

        team = self.teams[team_id]

        # Check if user has permission to manage roles
        if not self.has_permission(team_id, updated_by, Permission.MANAGE_ROLES):
            return False

        # Can't change the owner's role
        if user_id == team.owner_id:
            return False

        if user_id in team.members:
            member = team.members[user_id]
            member.role = new_role
            member.permissions = self.role_permissions[new_role]
            team.updated_at = datetime.now()
            self._save_data()

            logging.info(
                f"Updated member {user_id} role to {new_role.value} in team {team_id}"
            )
            return True

        return False

    def has_permission(
        self, team_id: str, user_id: str, permission: Permission
    ) -> bool:
        """Check if a user has a specific permission in a team."""
        if team_id not in self.teams:
            return False

        team = self.teams[team_id]

        if user_id not in team.members:
            return False

        member = team.members[user_id]
        return permission in member.permissions

    def get_member_permissions(self, team_id: str, user_id: str) -> Set[Permission]:
        """Get all permissions for a user in a team."""
        if team_id not in self.teams:
            return set()

        team = self.teams[team_id]

        if user_id not in team.members:
            return set()

        return team.members[user_id].permissions

    def create_invitation(
        self,
        team_id: str,
        email: str,
        role: TeamRole,
        invited_by: str,
        expires_in_days: int = 7,
    ) -> Optional[TeamInvitation]:
        """Create a team invitation."""
        if team_id not in self.teams:
            return None

        # Check if user has permission to invite members
        if not self.has_permission(team_id, invited_by, Permission.INVITE_MEMBERS):
            return None

        # Check if team is full
        team = self.teams[team_id]
        if len(team.members) >= team.max_members:
            return None

        invitation_id = str(uuid.uuid4())
        invitation = TeamInvitation(
            id=invitation_id,
            team_id=team_id,
            email=email,
            role=role,
            invited_by=invited_by,
            invited_at=datetime.now(),
            expires_at=datetime.now() + timedelta(days=expires_in_days),
        )

        self.invitations[invitation_id] = invitation
        self._save_data()

        logging.info(
            f"Created invitation {invitation_id} for {email} to team {team_id}"
        )
        return invitation

    def accept_invitation(
        self, invitation_id: str, user_id: str, username: str
    ) -> bool:
        """Accept a team invitation."""
        if invitation_id not in self.invitations:
            return False

        invitation = self.invitations[invitation_id]

        # Check if invitation is expired
        if datetime.now() > invitation.expires_at:
            return False

        # Check if invitation is already accepted
        if invitation.is_accepted:
            return False

        # Add user to team
        success = self.add_member(
            invitation.team_id,
            user_id,
            username,
            invitation.email,
            invitation.role,
            invitation.invited_by,
        )

        if success:
            invitation.is_accepted = True
            invitation.accepted_at = datetime.now()
            self._save_data()

            logging.info(f"Accepted invitation {invitation_id} by user {user_id}")
            return True

        return False

    def get_pending_invitations(self, email: str) -> List[TeamInvitation]:
        """Get pending invitations for an email."""
        return [
            invitation
            for invitation in self.invitations.values()
            if invitation.email == email
            and not invitation.is_accepted
            and datetime.now() <= invitation.expires_at
        ]

    def update_member_activity(self, team_id: str, user_id: str):
        """Update member's last activity time."""
        if team_id in self.teams and user_id in self.teams[team_id].members:
            self.teams[team_id].members[user_id].last_active = datetime.now()
            self._save_data()

    def get_team_analytics(
        self, team_id: str, user_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get team analytics (requires VIEW_ANALYTICS permission)."""
        if not self.has_permission(team_id, user_id, Permission.VIEW_ANALYTICS):
            return None

        if team_id not in self.teams:
            return None

        team = self.teams[team_id]

        # Calculate analytics
        total_members = len(team.members)
        active_members = len(
            [
                member
                for member in team.members.values()
                if member.last_active > datetime.now() - timedelta(days=7)
            ]
        )

        role_distribution = {}
        for member in team.members.values():
            role = member.role.value
            role_distribution[role] = role_distribution.get(role, 0) + 1

        return {
            "team_id": team_id,
            "total_members": total_members,
            "active_members": active_members,
            "activity_rate": (
                (active_members / total_members * 100) if total_members > 0 else 0
            ),
            "role_distribution": role_distribution,
            "created_at": team.created_at.isoformat(),
            "last_updated": team.updated_at.isoformat(),
        }


# Global team manager instance
team_manager = TeamManager()


def run(context=None):
    """Plugin entry point for testing the team manager."""
    # Create a test team
    team = team_manager.create_team(
        name="Test Development Team",
        description="A test team for collaborative development",
        owner_id="test_owner_1",
        owner_email="owner@test.com",
        is_public=False,
    )

    # Add some members
    team_manager.add_member(
        team.id,
        "test_member_1",
        "Alice Developer",
        "alice@test.com",
        TeamRole.EDITOR,
        "test_owner_1",
    )

    team_manager.add_member(
        team.id,
        "test_member_2",
        "Bob Reviewer",
        "bob@test.com",
        TeamRole.VIEWER,
        "test_owner_1",
    )

    # Create an invitation
    invitation = team_manager.create_invitation(
        team.id, "charlie@test.com", TeamRole.EDITOR, "test_owner_1"
    )

    # Test permissions
    can_edit = team_manager.has_permission(
        team.id, "test_member_1", Permission.EDIT_PROJECT
    )
    can_invite = team_manager.has_permission(
        team.id, "test_member_1", Permission.INVITE_MEMBERS
    )

    # Get analytics
    analytics = team_manager.get_team_analytics(team.id, "test_owner_1")

    return {
        "status": "success",
        "message": "Team manager test completed",
        "data": {
            "team_id": team.id,
            "team_info": {
                "name": team.name,
                "description": team.description,
                "member_count": len(team.members),
                "owner_id": team.owner_id,
            },
            "members": [
                {
                    "user_id": member.user_id,
                    "username": member.username,
                    "role": member.role.value,
                    "permissions": [p.value for p in member.permissions],
                }
                for member in team.members.values()
            ],
            "invitation": {
                "id": invitation.id if invitation else None,
                "email": invitation.email if invitation else None,
                "role": invitation.role.value if invitation else None,
            },
            "permission_tests": {
                "member_1_can_edit": can_edit,
                "member_1_can_invite": can_invite,
            },
            "analytics": analytics,
            "features": [
                "Role-based access control",
                "Team member management",
                "Invitation system",
                "Permission checking",
                "Team analytics",
                "Persistent storage",
            ],
        },
    }
