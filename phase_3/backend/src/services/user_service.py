from sqlmodel import Session, select
from typing import Optional
from ..models.user import User as UserModel, UserCreate, UserUpdate
from ..auth import hash_password, verify_password


class UserService:
    """
    Service class for managing user operations
    """

    @staticmethod
    def get_user_by_id(user_id: str, session: Session) -> Optional[UserModel]:
        """Get a user by their ID."""
        statement = select(UserModel).where(UserModel.id == user_id)
        return session.exec(statement).first()

    @staticmethod
    def get_user_by_email(email: str, session: Session) -> Optional[UserModel]:
        """Get a user by their email."""
        statement = select(UserModel).where(UserModel.email == email)
        return session.exec(statement).first()

    @staticmethod
    def create_user(user_data: UserCreate, session: Session) -> UserModel:
        """Create a new user."""
        # Hash the password
        hashed_password = hash_password(user_data.password)

        # Create the user object
        db_user = UserModel(
            email=user_data.email,
            name=user_data.name,
            hashed_password=hashed_password
        )

        # Add to session and commit
        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        return db_user

    @staticmethod
    def update_user(user_id: str, user_update: UserUpdate, session: Session) -> Optional[UserModel]:
        """Update a user's information."""
        db_user = UserService.get_user_by_id(user_id, session)

        if not db_user:
            return None

        # Update fields that were provided
        update_data = user_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)

        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        return db_user

    @staticmethod
    def delete_user(user_id: str, session: Session) -> bool:
        """Delete a user."""
        db_user = UserService.get_user_by_id(user_id, session)

        if not db_user:
            return False

        session.delete(db_user)
        session.commit()
        return True

    @staticmethod
    def authenticate_user(email: str, password: str, session: Session) -> Optional[UserModel]:
        """Authenticate a user by email and password."""
        db_user = UserService.get_user_by_email(email, session)

        if not db_user:
            return None

        if verify_password(password, db_user.hashed_password):
            return db_user

        return None

    @staticmethod
    def change_password(user_id: str, old_password: str, new_password: str, session: Session) -> bool:
        """Change a user's password."""
        db_user = UserService.get_user_by_id(user_id, session)

        if not db_user:
            return False

        # Verify old password
        if not verify_password(old_password, db_user.hashed_password):
            return False

        # Hash and update new password
        db_user.hashed_password = hash_password(new_password)
        session.add(db_user)
        session.commit()

        return True