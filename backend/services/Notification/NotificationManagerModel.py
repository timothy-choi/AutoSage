from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, ARRAY
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class NotificationManager(Base):
    __tablename__ = "notification_manager"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    notification_type = Column(String(100), nullable=False)
    show_notifications = Column(Boolean, default=True)
    all_user_notifications = Column(ARRAY(PG_UUID), nullable=True)
    user_token = Column(String(100), nullable=True)

    def to_dict(self):
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "notification_type": self.notification_type,
            "show_notifications": self.show_notifications,
            "all_user_notifications": [str(notification) for notification in self.all_user_notifications],
            "user_token": self.user_token
        }