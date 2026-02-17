from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlmodel import SQLModel, Field, create_engine, Session, select
from sqlalchemy import Column, JSON
import uuid

class NotificationRecord(SQLModel, table=True):
    """
    Model for storing notification records for audit trail
    """
    __tablename__ = "notifications"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    task_id: str
    user_id: str
    task_title: str
    message: str
    channels: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))  # Stores results for each channel
    sent_at: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class NotificationStorage:
    """
    Storage service for notification records
    """
    def __init__(self, database_url: str = "sqlite:///./notifications.db"):
        self.engine = create_engine(database_url, echo=True)
        SQLModel.metadata.create_all(self.engine)

    def save_notification_record(
        self,
        task_id: str,
        user_id: str,
        task_title: str,
        message: str,
        channels: Dict[str, Any]
    ) -> NotificationRecord:
        """
        Save a notification record to the database
        """
        record = NotificationRecord(
            task_id=task_id,
            user_id=user_id,
            task_title=task_title,
            message=message,
            channels=channels
        )

        with Session(self.engine) as session:
            session.add(record)
            session.commit()
            session.refresh(record)
            return record

    def get_notifications_by_task(self, task_id: str) -> List[NotificationRecord]:
        """
        Get all notifications for a specific task
        """
        with Session(self.engine) as session:
            statement = select(NotificationRecord).where(NotificationRecord.task_id == task_id)
            return session.exec(statement).all()

    def get_notifications_by_user(self, user_id: str) -> List[NotificationRecord]:
        """
        Get all notifications for a specific user
        """
        with Session(self.engine) as session:
            statement = select(NotificationRecord).where(NotificationRecord.user_id == user_id)
            return session.exec(statement).all()

    def get_recent_notifications(self, limit: int = 100) -> List[NotificationRecord]:
        """
        Get recent notifications
        """
        with Session(self.engine) as session:
            statement = select(NotificationRecord).order_by(NotificationRecord.created_at.desc()).limit(limit)
            return session.exec(statement).all()

    def cleanup_old_notifications(self, days_old: int = 30) -> int:
        """
        Clean up notification records older than specified days
        """
        from datetime import timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=days_old)

        with Session(self.engine) as session:
            statement = select(NotificationRecord).where(NotificationRecord.created_at < cutoff_date)
            old_records = session.exec(statement).all()

            for record in old_records:
                session.delete(record)

            session.commit()
            return len(old_records)

# Global instance
notification_storage = NotificationStorage()