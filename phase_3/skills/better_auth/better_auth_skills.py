"""
Better Auth Skills
This module provides skills for authentication and authorization using Better Auth.
"""
import asyncio
import json
from typing import Dict, Any, Optional, List
import uuid
from datetime import datetime, timedelta
import hashlib
import secrets


class BetterAuthSkills:
    """
    Skills for working with Better Auth.
    These skills provide high-level operations for authentication and authorization.
    """

    def __init__(self):
        self.skill_name = "better_auth_skills"
        self.description = "Skills for authentication and authorization using Better Auth"
        # In-memory storage for demonstration (in production, this would connect to the actual Better Auth service)
        self.users: Dict[str, Dict[str, Any]] = {}
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.organizations: Dict[str, Dict[str, Any]] = {}
        self.rate_limits: Dict[str, Dict[str, Any]] = {}

    async def create_user(self, email: str, password: str, name: Optional[str] = None,
                         metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create a new user with email and password authentication.

        Args:
            email: User's email address
            password: User's password (will be hashed)
            name: User's name (optional)
            metadata: Additional user metadata (optional)

        Returns:
            Dictionary containing user information or error information
        """
        try:
            # Validate required parameters
            if not email or not password:
                return {
                    "error": "Both 'email' and 'password' are required parameters"
                }

            # Check if user already exists
            if email in [user['email'] for user in self.users.values()]:
                return {
                    "error": f"User with email {email} already exists"
                }

            # Generate user ID
            user_id = str(uuid.uuid4())

            # Hash the password (in production, use proper password hashing)
            password_hash = hashlib.sha256(password.encode()).hexdigest()

            # Create user record
            user_data = {
                "id": user_id,
                "email": email,
                "password_hash": password_hash,
                "name": name or email.split('@')[0],  # Use part of email as name if not provided
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
                "email_verified": False,
                "metadata": metadata or {},
                "two_factor_enabled": False
            }

            self.users[user_id] = user_data

            return {
                "success": True,
                "user": user_data,
                "message": f"User {email} created successfully"
            }

        except Exception as e:
            return {"error": f"Failed to create user: {str(e)}"}

    async def authenticate_user(self, email: str, password: str) -> Dict[str, Any]:
        """
        Authenticate a user with email and password.

        Args:
            email: User's email address
            password: User's password

        Returns:
            Dictionary containing authentication result or error information
        """
        try:
            # Find user by email
            user = None
            for user_data in self.users.values():
                if user_data["email"] == email:
                    user = user_data
                    break

            if not user:
                return {
                    "error": "Invalid email or password"
                }

            # Hash the provided password and compare
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            if password_hash != user["password_hash"]:
                return {
                    "error": "Invalid email or password"
                }

            # Check if 2FA is required
            if user.get("two_factor_enabled", False):
                return {
                    "success": True,
                    "requires_2fa": True,
                    "user_id": user["id"],
                    "message": "Authentication successful, 2FA required"
                }

            # Create a session
            session_id = str(uuid.uuid4())
            session_data = {
                "id": session_id,
                "user_id": user["id"],
                "created_at": datetime.utcnow().isoformat(),
                "expires_at": (datetime.utcnow() + timedelta(hours=24)).isoformat(),
                "ip_address": "127.0.0.1",  # In real implementation, this would come from request
                "user_agent": "Better Auth Skill"
            }

            self.sessions[session_id] = session_data

            return {
                "success": True,
                "user": user,
                "session": session_data,
                "message": "Authentication successful"
            }

        except Exception as e:
            return {"error": f"Failed to authenticate user: {str(e)}"}

    async def create_session(self, user_id: str) -> Dict[str, Any]:
        """
        Create a new session for a user.

        Args:
            user_id: ID of the user to create session for

        Returns:
            Dictionary containing session information or error information
        """
        try:
            if user_id not in self.users:
                return {
                    "error": f"User with ID {user_id} not found"
                }

            # Create a session
            session_id = str(uuid.uuid4())
            session_data = {
                "id": session_id,
                "user_id": user_id,
                "created_at": datetime.utcnow().isoformat(),
                "expires_at": (datetime.utcnow() + timedelta(hours=24)).isoformat(),
                "ip_address": "127.0.0.1",  # In real implementation, this would come from request
                "user_agent": "Better Auth Skill"
            }

            self.sessions[session_id] = session_data

            return {
                "success": True,
                "session": session_data,
                "message": f"Session created for user {user_id}"
            }

        except Exception as e:
            return {"error": f"Failed to create session: {str(e)}"}

    async def verify_session(self, session_id: str) -> Dict[str, Any]:
        """
        Verify if a session is valid.

        Args:
            session_id: ID of the session to verify

        Returns:
            Dictionary containing session verification result or error information
        """
        try:
            if session_id not in self.sessions:
                return {
                    "error": f"Session with ID {session_id} not found"
                }

            session_data = self.sessions[session_id]
            expires_at = datetime.fromisoformat(session_data["expires_at"].replace('Z', '+00:00'))

            if datetime.utcnow() > expires_at:
                # Session expired, remove it
                del self.sessions[session_id]
                return {
                    "error": "Session has expired"
                }

            # Get user information
            user_id = session_data["user_id"]
            if user_id not in self.users:
                return {
                    "error": f"User with ID {user_id} not found"
                }

            return {
                "success": True,
                "session": session_data,
                "user": self.users[user_id],
                "message": "Session is valid"
            }

        except Exception as e:
            return {"error": f"Failed to verify session: {str(e)}"}

    async def create_organization(self, name: str, owner_user_id: str,
                                metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create a new organization.

        Args:
            name: Name of the organization
            owner_user_id: ID of the user who will be the owner
            metadata: Additional organization metadata (optional)

        Returns:
            Dictionary containing organization information or error information
        """
        try:
            if owner_user_id not in self.users:
                return {
                    "error": f"User with ID {owner_user_id} not found"
                }

            # Generate organization ID
            org_id = str(uuid.uuid4())

            # Create organization record
            org_data = {
                "id": org_id,
                "name": name,
                "owner_id": owner_user_id,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
                "metadata": metadata or {},
                "members": [owner_user_id],  # Owner is automatically a member
                "roles": {
                    owner_user_id: "owner"  # Owner gets owner role by default
                }
            }

            self.organizations[org_id] = org_data

            return {
                "success": True,
                "organization": org_data,
                "message": f"Organization {name} created successfully"
            }

        except Exception as e:
            return {"error": f"Failed to create organization: {str(e)}"}

    async def add_user_to_organization(self, org_id: str, user_id: str, role: str = "member") -> Dict[str, Any]:
        """
        Add a user to an organization.

        Args:
            org_id: ID of the organization
            user_id: ID of the user to add
            role: Role to assign to the user (default: "member")

        Returns:
            Dictionary containing result or error information
        """
        try:
            if org_id not in self.organizations:
                return {
                    "error": f"Organization with ID {org_id} not found"
                }

            if user_id not in self.users:
                return {
                    "error": f"User with ID {user_id} not found"
                }

            org_data = self.organizations[org_id]

            # Add user to organization if not already a member
            if user_id not in org_data["members"]:
                org_data["members"].append(user_id)
                org_data["roles"][user_id] = role
                org_data["updated_at"] = datetime.utcnow().isoformat()

                return {
                    "success": True,
                    "organization": org_data,
                    "message": f"User {user_id} added to organization {org_data['name']} with role {role}"
                }
            else:
                # Update role if user is already a member
                org_data["roles"][user_id] = role
                org_data["updated_at"] = datetime.utcnow().isoformat()

                return {
                    "success": True,
                    "organization": org_data,
                    "message": f"User {user_id} role updated to {role} in organization {org_data['name']}"
                }

        except Exception as e:
            return {"error": f"Failed to add user to organization: {str(e)}"}

    async def enable_two_factor(self, user_id: str, method: str = "totp") -> Dict[str, Any]:
        """
        Enable two-factor authentication for a user.

        Args:
            user_id: ID of the user
            method: 2FA method (default: "totp")

        Returns:
            Dictionary containing result or error information
        """
        try:
            if user_id not in self.users:
                return {
                    "error": f"User with ID {user_id} not found"
                }

            # Generate a secret for TOTP (in real implementation, this would be a proper TOTP secret)
            secret = secrets.token_urlsafe(32)

            self.users[user_id]["two_factor_enabled"] = True
            self.users[user_id]["two_factor_method"] = method
            self.users[user_id]["two_factor_secret"] = secret
            self.users[user_id]["updated_at"] = datetime.utcnow().isoformat()

            return {
                "success": True,
                "user_id": user_id,
                "method": method,
                "secret": secret,  # In real implementation, this would be returned in a secure way
                "message": f"Two-factor authentication enabled for user {user_id} using {method}"
            }

        except Exception as e:
            return {"error": f"Failed to enable two-factor authentication: {str(e)}"}

    async def rate_limit_check(self, identifier: str, limit: int = 10, window: int = 60) -> Dict[str, Any]:
        """
        Check if a rate limit has been exceeded.

        Args:
            identifier: Identifier for the rate limit (e.g., IP address, user ID)
            limit: Number of requests allowed (default: 10)
            window: Time window in seconds (default: 60)

        Returns:
            Dictionary containing rate limit status or error information
        """
        try:
            current_time = datetime.utcnow().timestamp()
            window_start = current_time - window

            if identifier not in self.rate_limits:
                self.rate_limits[identifier] = {
                    "requests": [],
                    "limit": limit,
                    "window": window
                }

            # Remove old requests outside the window
            self.rate_limits[identifier]["requests"] = [
                req_time for req_time in self.rate_limits[identifier]["requests"]
                if req_time > window_start
            ]

            # Add current request
            self.rate_limits[identifier]["requests"].append(current_time)

            # Check if limit is exceeded
            current_count = len(self.rate_limits[identifier]["requests"])

            return {
                "success": True,
                "identifier": identifier,
                "current_count": current_count,
                "limit": limit,
                "window": window,
                "allowed": current_count <= limit,
                "remaining": max(0, limit - current_count),
                "reset_time": window_start + window
            }

        except Exception as e:
            return {"error": f"Failed to check rate limit: {str(e)}"}

    async def get_user_by_id(self, user_id: str) -> Dict[str, Any]:
        """
        Get user information by ID.

        Args:
            user_id: ID of the user to retrieve

        Returns:
            Dictionary containing user information or error information
        """
        try:
            if user_id not in self.users:
                return {
                    "error": f"User with ID {user_id} not found"
                }

            # Return user data without sensitive information
            user_data = self.users[user_id].copy()
            if "password_hash" in user_data:
                del user_data["password_hash"]

            return {
                "success": True,
                "user": user_data
            }

        except Exception as e:
            return {"error": f"Failed to get user: {str(e)}"}

    async def update_user(self, user_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update user information.

        Args:
            user_id: ID of the user to update
            updates: Dictionary of fields to update

        Returns:
            Dictionary containing updated user information or error information
        """
        try:
            if user_id not in self.users:
                return {
                    "error": f"User with ID {user_id} not found"
                }

            # Update user data
            for key, value in updates.items():
                if key in ["email", "name", "metadata", "email_verified"]:
                    self.users[user_id][key] = value

            self.users[user_id]["updated_at"] = datetime.utcnow().isoformat()

            # Return updated user data without sensitive information
            user_data = self.users[user_id].copy()
            if "password_hash" in user_data:
                del user_data["password_hash"]

            return {
                "success": True,
                "user": user_data,
                "message": f"User {user_id} updated successfully"
            }

        except Exception as e:
            return {"error": f"Failed to update user: {str(e)}"}


# Singleton instance
better_auth_skills = BetterAuthSkills()


async def create_user(email: str, password: str, name: Optional[str] = None,
                     metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Skill to create a new user with email and password authentication."""
    return await better_auth_skills.create_user(email, password, name, metadata)


async def authenticate_user(email: str, password: str) -> Dict[str, Any]:
    """Skill to authenticate a user with email and password."""
    return await better_auth_skills.authenticate_user(email, password)


async def create_session(user_id: str) -> Dict[str, Any]:
    """Skill to create a new session for a user."""
    return await better_auth_skills.create_session(user_id)


async def verify_session(session_id: str) -> Dict[str, Any]:
    """Skill to verify if a session is valid."""
    return await better_auth_skills.verify_session(session_id)


async def create_organization(name: str, owner_user_id: str,
                            metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Skill to create a new organization."""
    return await better_auth_skills.create_organization(name, owner_user_id, metadata)


async def add_user_to_organization(org_id: str, user_id: str, role: str = "member") -> Dict[str, Any]:
    """Skill to add a user to an organization."""
    return await better_auth_skills.add_user_to_organization(org_id, user_id, role)


async def enable_two_factor(user_id: str, method: str = "totp") -> Dict[str, Any]:
    """Skill to enable two-factor authentication for a user."""
    return await better_auth_skills.enable_two_factor(user_id, method)


async def rate_limit_check(identifier: str, limit: int = 10, window: int = 60) -> Dict[str, Any]:
    """Skill to check if a rate limit has been exceeded."""
    return await better_auth_skills.rate_limit_check(identifier, limit, window)


async def get_user_by_id(user_id: str) -> Dict[str, Any]:
    """Skill to get user information by ID."""
    return await better_auth_skills.get_user_by_id(user_id)


async def update_user(user_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
    """Skill to update user information."""
    return await better_auth_skills.update_user(user_id, updates)


# Example usage
async def main():
    """Example of using the Better Auth skills."""
    print("Testing Better Auth Skills")
    print("=" * 40)

    # Create a user
    user_result = await create_user(
        email="test@example.com",
        password="securepassword123",
        name="Test User",
        metadata={"department": "engineering"}
    )
    print(f"User creation: {user_result['success'] if user_result.get('success') else 'Failed'}")

    if user_result.get('success'):
        user_id = user_result['user']['id']
        print(f"Created user ID: {user_id[:8]}...")

        # Authenticate the user
        auth_result = await authenticate_user("test@example.com", "securepassword123")
        print(f"Authentication: {auth_result['success'] if auth_result.get('success') else 'Failed'}")

        if auth_result.get('success') and not auth_result.get('requires_2fa'):
            session_id = auth_result['session']['id']
            print(f"Created session ID: {session_id[:8]}...")

            # Verify the session
            verify_result = await verify_session(session_id)
            print(f"Session verification: {verify_result['success'] if verify_result.get('success') else 'Failed'}")

        # Create an organization
        org_result = await create_organization(
            name="Test Organization",
            owner_user_id=user_id,
            metadata={"industry": "tech"}
        )
        print(f"Organization creation: {org_result['success'] if org_result.get('success') else 'Failed'}")

        if org_result.get('success'):
            org_id = org_result['organization']['id']
            print(f"Created organization ID: {org_id[:8]}...")

        # Enable 2FA for the user
        tfa_result = await enable_two_factor(user_id)
        print(f"2FA enable: {tfa_result['success'] if tfa_result.get('success') else 'Failed'}")

        # Check rate limiting
        rate_result = await rate_limit_check("test-user-123", limit=5, window=60)
        print(f"Rate limit check: {rate_result['allowed'] if rate_result.get('success') else 'Failed'}")

    print("\nBetter Auth skills are ready to handle authentication and authorization!")


if __name__ == "__main__":
    asyncio.run(main())