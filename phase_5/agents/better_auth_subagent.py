#!/usr/bin/env python3
"""
Better Auth Subagent
This subagent specializes in authentication and authorization using Better Auth.
"""
import asyncio
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import the Better Auth skills
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from skills.better_auth.better_auth_skills import (
        create_user,
        authenticate_user,
        create_session,
        verify_session,
        create_organization,
        add_user_to_organization,
        enable_two_factor,
        rate_limit_check,
        get_user_by_id,
        update_user
    )
except ImportError as e:
    logger.warning(f"Better Auth skills not available: {e}. Please install the skills first.")
    # Define dummy functions for testing
    async def create_user(*args, **kwargs):
        return {"success": False, "error": "Skills not available", "user": {"id": "dummy", "email": kwargs.get("email", "test@example.com")}}
    async def authenticate_user(*args, **kwargs):
        return {"success": False, "error": "Skills not available"}
    async def create_session(*args, **kwargs):
        return {"success": False, "error": "Skills not available"}
    async def verify_session(*args, **kwargs):
        return {"success": False, "error": "Skills not available"}
    async def create_organization(*args, **kwargs):
        return {"success": False, "error": "Skills not available"}
    async def add_user_to_organization(*args, **kwargs):
        return {"success": False, "error": "Skills not available"}
    async def enable_two_factor(*args, **kwargs):
        return {"success": False, "error": "Skills not available"}
    async def rate_limit_check(*args, **kwargs):
        return {"success": False, "error": "Skills not available"}
    async def get_user_by_id(*args, **kwargs):
        return {"success": False, "error": "Skills not available"}
    async def update_user(*args, **kwargs):
        return {"success": False, "error": "Skills not available"}


class BetterAuthSubagent:
    """
    Better Auth Subagent - Specializes in authentication and authorization using Better Auth.
    """
    def __init__(self):
        self.subagent_id = str(uuid.uuid4())
        self.name = "better_auth_subagent"
        self.description = "Better Auth Manager - Handles authentication and authorization using Better Auth"
        self.capabilities = [
            "create-user",
            "authenticate-user",
            "manage-sessions",
            "create-organization",
            "manage-organization-members",
            "enable-two-factor",
            "rate-limiting",
            "user-management"
        ]
        self.users_registry: Dict[str, Dict[str, Any]] = {}
        self.sessions_registry: Dict[str, Dict[str, Any]] = {}
        self.organizations_registry: Dict[str, Dict[str, Any]] = {}

    async def create_user(self, email: str, password: str, name: Optional[str] = None,
                         metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a new user with email and password authentication."""
        try:
            result = await create_user(email, password, name, metadata)

            if result.get("success"):
                user_data = result["user"]
                user_id = user_data["id"]

                # Register the user in our internal registry
                self.users_registry[user_id] = {
                    "id": user_id,
                    "email": email,
                    "name": name or email.split('@')[0],
                    "created_at": datetime.utcnow().isoformat(),
                    "metadata": metadata or {},
                    "type": "user"
                }

                logger.info(f"Created user '{email}' with ID: {user_id}")

                return {
                    "success": True,
                    "user_id": user_id,
                    "user_data": user_data,
                    "message": f"User '{email}' created successfully with ID {user_id}"
                }
            else:
                return result

        except Exception as e:
            logger.error(f"Failed to create user: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    async def authenticate_user(self, email: str, password: str) -> Dict[str, Any]:
        """Authenticate a user with email and password."""
        try:
            result = await authenticate_user(email, password)

            if result.get("success"):
                if result.get("requires_2fa"):
                    return {
                        "success": True,
                        "user_id": result["user_id"],
                        "requires_2fa": True,
                        "message": "Authentication successful, 2FA required"
                    }
                else:
                    user_data = result["user"]
                    session_data = result["session"]

                    # Register the session in our internal registry
                    self.sessions_registry[session_data["id"]] = {
                        "id": session_data["id"],
                        "user_id": user_data["id"],
                        "created_at": session_data["created_at"],
                        "expires_at": session_data["expires_at"],
                        "type": "session"
                    }

                    return {
                        "success": True,
                        "user_data": user_data,
                        "session_data": session_data,
                        "message": f"Authentication successful for user {email}"
                    }
            else:
                return result

        except Exception as e:
            logger.error(f"Failed to authenticate user: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    async def create_session(self, user_id: str) -> Dict[str, Any]:
        """Create a new session for a user."""
        try:
            result = await create_session(user_id)

            if result.get("success"):
                session_data = result["session"]

                # Register the session in our internal registry
                self.sessions_registry[session_data["id"]] = {
                    "id": session_data["id"],
                    "user_id": user_id,
                    "created_at": session_data["created_at"],
                    "expires_at": session_data["expires_at"],
                    "type": "session"
                }

                logger.info(f"Created session for user '{user_id}' with ID: {session_data['id']}")

                return {
                    "success": True,
                    "session_id": session_data["id"],
                    "session_data": session_data,
                    "message": f"Session created successfully for user {user_id}"
                }
            else:
                return result

        except Exception as e:
            logger.error(f"Failed to create session: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    async def verify_session(self, session_id: str) -> Dict[str, Any]:
        """Verify if a session is valid."""
        try:
            result = await verify_session(session_id)

            if result.get("success"):
                session_data = result["session"]
                user_data = result["user"]

                return {
                    "success": True,
                    "session_data": session_data,
                    "user_data": user_data,
                    "message": f"Session {session_id} is valid"
                }
            else:
                return result

        except Exception as e:
            logger.error(f"Failed to verify session: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    async def create_organization(self, name: str, owner_user_id: str,
                                metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a new organization."""
        try:
            result = await create_organization(name, owner_user_id, metadata)

            if result.get("success"):
                org_data = result["organization"]
                org_id = org_data["id"]

                # Register the organization in our internal registry
                self.organizations_registry[org_id] = {
                    "id": org_id,
                    "name": name,
                    "owner_id": owner_user_id,
                    "created_at": datetime.utcnow().isoformat(),
                    "members": org_data["members"],
                    "roles": org_data["roles"],
                    "metadata": metadata or {},
                    "type": "organization"
                }

                logger.info(f"Created organization '{name}' with ID: {org_id}")

                return {
                    "success": True,
                    "org_id": org_id,
                    "org_data": org_data,
                    "message": f"Organization '{name}' created successfully with ID {org_id}"
                }
            else:
                return result

        except Exception as e:
            logger.error(f"Failed to create organization: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    async def add_user_to_organization(self, org_id: str, user_id: str, role: str = "member") -> Dict[str, Any]:
        """Add a user to an organization."""
        try:
            result = await add_user_to_organization(org_id, user_id, role)

            if result.get("success"):
                org_data = result["organization"]

                # Update the organization in our registry
                self.organizations_registry[org_id] = {
                    "id": org_id,
                    "name": org_data["name"],
                    "owner_id": org_data["owner_id"],
                    "created_at": org_data["created_at"],
                    "updated_at": org_data["updated_at"],
                    "members": org_data["members"],
                    "roles": org_data["roles"],
                    "metadata": org_data["metadata"],
                    "type": "organization"
                }

                return {
                    "success": True,
                    "org_data": org_data,
                    "message": f"User {user_id} added to organization {org_data['name']} with role {role}"
                }
            else:
                return result

        except Exception as e:
            logger.error(f"Failed to add user to organization: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    async def enable_two_factor(self, user_id: str, method: str = "totp") -> Dict[str, Any]:
        """Enable two-factor authentication for a user."""
        try:
            result = await enable_two_factor(user_id, method)

            if result.get("success"):
                return {
                    "success": True,
                    "user_id": user_id,
                    "method": method,
                    "secret": result["secret"],
                    "message": f"Two-factor authentication enabled for user {user_id} using {method}"
                }
            else:
                return result

        except Exception as e:
            logger.error(f"Failed to enable two-factor authentication: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    async def rate_limit_check(self, identifier: str, limit: int = 10, window: int = 60) -> Dict[str, Any]:
        """Check if a rate limit has been exceeded."""
        try:
            result = await rate_limit_check(identifier, limit, window)

            return result

        except Exception as e:
            logger.error(f"Failed to check rate limit: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    async def get_user_info(self, user_id: str) -> Dict[str, Any]:
        """Get information about a specific user."""
        try:
            if user_id not in self.users_registry:
                return {
                    "success": False,
                    "error": f"User with ID '{user_id}' not found in registry"
                }

            user_info = self.users_registry[user_id]

            return {
                "success": True,
                "user_info": user_info
            }

        except Exception as e:
            logger.error(f"Failed to get user info: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    async def list_users(self) -> Dict[str, Any]:
        """List all registered users."""
        try:
            users_list = []
            for user_id, user_data in self.users_registry.items():
                users_list.append({
                    "id": user_id,
                    "email": user_data["email"],
                    "name": user_data["name"],
                    "created_at": user_data["created_at"]
                })

            return {
                "success": True,
                "users_count": len(users_list),
                "users": users_list
            }

        except Exception as e:
            logger.error(f"Failed to list users: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    async def list_sessions(self) -> Dict[str, Any]:
        """List all active sessions."""
        try:
            sessions_list = []
            current_time = datetime.utcnow().isoformat()

            for session_id, session_data in self.sessions_registry.items():
                # Check if session is still valid
                if session_data["expires_at"] > current_time:
                    sessions_list.append({
                        "id": session_id,
                        "user_id": session_data["user_id"],
                        "created_at": session_data["created_at"],
                        "expires_at": session_data["expires_at"]
                    })

            return {
                "success": True,
                "sessions_count": len(sessions_list),
                "sessions": sessions_list
            }

        except Exception as e:
            logger.error(f"Failed to list sessions: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    async def list_organizations(self) -> Dict[str, Any]:
        """List all registered organizations."""
        try:
            orgs_list = []
            for org_id, org_data in self.organizations_registry.items():
                orgs_list.append({
                    "id": org_id,
                    "name": org_data["name"],
                    "owner_id": org_data["owner_id"],
                    "members_count": len(org_data["members"]),
                    "created_at": org_data["created_at"]
                })

            return {
                "success": True,
                "organizations_count": len(orgs_list),
                "organizations": orgs_list
            }

        except Exception as e:
            logger.error(f"Failed to list organizations: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    async def handle_task(self, task_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming tasks for the Better Auth subagent."""
        try:
            if task_name == "create_user":
                email = arguments.get("email")
                password = arguments.get("password")
                name = arguments.get("name")
                metadata = arguments.get("metadata", {})

                if not email or not password:
                    return {
                        "success": False,
                        "error": "Both 'email' and 'password' are required"
                    }

                return await self.create_user(email, password, name, metadata)

            elif task_name == "authenticate_user":
                email = arguments.get("email")
                password = arguments.get("password")

                if not email or not password:
                    return {
                        "success": False,
                        "error": "Both 'email' and 'password' are required"
                    }

                return await self.authenticate_user(email, password)

            elif task_name == "create_session":
                user_id = arguments.get("user_id")

                if not user_id:
                    return {
                        "success": False,
                        "error": "'user_id' is required"
                    }

                return await self.create_session(user_id)

            elif task_name == "verify_session":
                session_id = arguments.get("session_id")

                if not session_id:
                    return {
                        "success": False,
                        "error": "'session_id' is required"
                    }

                return await self.verify_session(session_id)

            elif task_name == "create_organization":
                name = arguments.get("name")
                owner_user_id = arguments.get("owner_user_id")
                metadata = arguments.get("metadata", {})

                if not name or not owner_user_id:
                    return {
                        "success": False,
                        "error": "Both 'name' and 'owner_user_id' are required"
                    }

                return await self.create_organization(name, owner_user_id, metadata)

            elif task_name == "add_user_to_organization":
                org_id = arguments.get("org_id")
                user_id = arguments.get("user_id")
                role = arguments.get("role", "member")

                if not org_id or not user_id:
                    return {
                        "success": False,
                        "error": "Both 'org_id' and 'user_id' are required"
                    }

                return await self.add_user_to_organization(org_id, user_id, role)

            elif task_name == "enable_two_factor":
                user_id = arguments.get("user_id")
                method = arguments.get("method", "totp")

                if not user_id:
                    return {
                        "success": False,
                        "error": "'user_id' is required"
                    }

                return await self.enable_two_factor(user_id, method)

            elif task_name == "rate_limit_check":
                identifier = arguments.get("identifier")
                limit = arguments.get("limit", 10)
                window = arguments.get("window", 60)

                if not identifier:
                    return {
                        "success": False,
                        "error": "'identifier' is required"
                    }

                return await self.rate_limit_check(identifier, limit, window)

            elif task_name == "get_user_info":
                user_id = arguments.get("user_id")

                if not user_id:
                    return {
                        "success": False,
                        "error": "'user_id' is required"
                    }

                return await self.get_user_info(user_id)

            elif task_name == "list_users":
                return await self.list_users()

            elif task_name == "list_sessions":
                return await self.list_sessions()

            elif task_name == "list_organizations":
                return await self.list_organizations()

            else:
                return {
                    "success": False,
                    "error": f"Unknown task: {task_name}"
                }

        except Exception as e:
            logger.error(f"Error handling task {task_name}: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }


async def run_better_auth_subagent():
    """
    Run the Better Auth Subagent as a standalone component
    """
    print("Initializing Better Auth Subagent...")
    print("=" * 60)

    # Create the subagent instance
    subagent = BetterAuthSubagent()

    print("+ Better Auth Subagent initialized successfully!")
    print(f"  - Subagent ID: {subagent.subagent_id}")
    print(f"  - Subagent Name: {subagent.name}")
    print(f"  - Description: {subagent.description}")
    print(f"  - Capabilities: {len(subagent.capabilities)}")
    for cap in subagent.capabilities:
        print(f"    * {cap}")

    # Demonstrate the subagent functionality
    print("\nDemonstrating subagent functionality:")

    # Create a user
    user_result = await subagent.create_user(
        email="admin@example.com",
        password="securePassword123",
        name="Admin User",
        metadata={"department": "admin"}
    )
    if user_result["success"]:
        user_id = user_result["user_id"]
        print(f"  + Created user: {user_result['user_data']['email']} (ID: {user_id[:8]}...)")
    else:
        print(f"  X Failed to create user: {user_result['error']}")

    # Authenticate the user
    if 'user_id' in locals():
        auth_result = await subagent.authenticate_user("admin@example.com", "securePassword123")
        if auth_result["success"]:
            if auth_result.get("requires_2fa"):
                print(f"  + Authentication successful, 2FA required for user: {auth_result['user_id'][:8]}...")
            else:
                session_id = auth_result["session_data"]["id"]
                print(f"  + Authenticated user, created session: {session_id[:8]}...")
        else:
            print(f"  X Failed to authenticate user: {auth_result['error']}")

    # Create an organization
    if 'user_id' in locals():
        org_result = await subagent.create_organization(
            name="Test Organization",
            owner_user_id=user_id,
            metadata={"industry": "technology"}
        )
        if org_result["success"]:
            org_id = org_result["org_id"]
            print(f"  + Created organization: {org_result['org_data']['name']} (ID: {org_id[:8]}...)")
        else:
            print(f"  X Failed to create organization: {org_result['error']}")

    # Enable 2FA for the user
    if 'user_id' in locals():
        tfa_result = await subagent.enable_two_factor(user_id)
        if tfa_result["success"]:
            print(f"  + Enabled 2FA for user: {user_id[:8]}... (method: {tfa_result['method']})")
        else:
            print(f"  X Failed to enable 2FA: {tfa_result['error']}")

    # Check rate limiting
    rate_result = await subagent.rate_limit_check("test-user-123", limit=5, window=60)
    if rate_result["success"]:
        print(f"  + Rate limit check for test-user-123: {rate_result['remaining']} requests remaining")
    else:
        print(f"  X Failed rate limit check: {rate_result['error']}")

    # List all created entities
    users_list = await subagent.list_users()
    if users_list["success"]:
        print(f"\n  + Total users created: {users_list['users_count']}")
        for user in users_list["users"]:
            print(f"    - {user['name']} ({user['email']}): {user['id'][:8]}...")

    orgs_list = await subagent.list_organizations()
    if orgs_list["success"] and orgs_list["organizations_count"] > 0:
        print(f"  + Total organizations created: {orgs_list['organizations_count']}")
        for org in orgs_list["organizations"]:
            print(f"    - {org['name']}: {org['id'][:8]}...")

    sessions_list = await subagent.list_sessions()
    if sessions_list["success"]:
        print(f"  + Total active sessions: {sessions_list['sessions_count']}")

    print("\n+ Better Auth Subagent is ready to handle authentication and authorization requests!")
    print("Use the subagent instance to call create_user(), authenticate_user(), or handle_task() methods.")

    return subagent


if __name__ == "__main__":
    try:
        subagent = asyncio.run(run_better_auth_subagent())
        print("\nSubagent is running and ready to handle requests!")
    except Exception as e:
        print(f"\nX Error running Better Auth Subagent: {e}")
        import traceback
        traceback.print_exc()