from sqlmodel import Session, select
from typing import Optional
from datetime import datetime, timedelta
import uuid
from ..models.user import User
from ..auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, verify_custom_token as verify_token
from fastapi import Depends, HTTPException, status


class SessionService:
    @staticmethod
    def create_session(user_id: str, session: Session, expires_in_hours: int = 24) -> str:
        """
        Create a session for a user and return a session token.
        """
        # In a real implementation, you might store session details in a database
        # For now, we're just creating a JWT token with expiration

        access_token_expires = timedelta(hours=expires_in_hours)
        token = create_access_token(
            data={"sub": user_id},
            expires_delta=access_token_expires
        )

        return token

    @staticmethod
    def validate_session(token: str) -> Optional[str]:
        """
        Validate a session token and return user_id if valid.
        """
        try:
            user = verify_token(token)
            return user.id
        except Exception:
            return None

    @staticmethod
    def refresh_session(token: str, session: Session) -> str:
        """
        Refresh a session token.
        """
        try:
            user = verify_token(token)

            # Create a new token with fresh expiration
            new_token = create_access_token(
                data={"sub": user.id, "email": user.email, "name": user.name},
                expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            )

            return new_token
        except Exception as e:
            raise e


class RBACService:
    """
    Role-Based Access Control service for managing user permissions.
    """

    # Define roles and permissions
    ROLES_PERMISSIONS = {
        "admin": [
            "read:user",
            "write:user",
            "delete:user",
            "read:task",
            "write:task",
            "delete:task",
            "read:conversation",
            "write:conversation",
            "delete:conversation",
            "read:message",
            "write:message",
            "delete:message"
        ],
        "user": [
            "read:user",
            "write:task",
            "read:conversation",
            "write:conversation",
            "read:message",
            "write:message"
        ],
        "guest": [
            "read:user"
        ]
    }

    @staticmethod
    def get_user_roles(user_id: str, session: Session) -> list:
        """
        Get roles for a user. In a real implementation, this would query the database.
        For now, we'll assign a default role based on user existence.
        """
        # In a real implementation, this would fetch roles from a database
        # Here we'll just return 'user' role for all registered users
        statement = select(User).where(User.id == user_id)
        db_user = session.exec(statement).first()

        if db_user:
            return ["user"]
        else:
            return ["guest"]

    @staticmethod
    def has_permission(user_id: str, permission: str, session: Session) -> bool:
        """
        Check if a user has a specific permission.
        """
        user_roles = RBACService.get_user_roles(user_id, session)

        for role in user_roles:
            if role in RBACService.ROLES_PERMISSIONS:
                if permission in RBACService.ROLES_PERMISSIONS[role]:
                    return True

        return False

    @staticmethod
    def require_permission(permission: str):
        """
        Dependency to require a specific permission.
        """
        from ..auth import get_current_user
        from ..database.connection import get_session

        def permission_dependency(
            current_user: User = Depends(get_current_user),
            session: Session = Depends(get_session)
        ):
            if not RBACService.has_permission(current_user.id, permission, session):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions"
                )
            return current_user
        return permission_dependency