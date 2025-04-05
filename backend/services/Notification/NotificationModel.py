from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class Notification(Base):
    __tablename__ = "notification"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    recipient_id = Column(PG_UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    recipient_username = Column(String(100), nullable=False)
    date_sent = Column(DateTime, nullable=False)
    title = Column(String(200), nullable=False)
    message = Column(String(500), nullable=False)
    redirectLink = Column(String(400), nullable=True)

    def to_dict(self):
        return {
            "id": str(self.id),
            "recipient_id": str(self.recipient_id),
            "recipient_username": self.recipient_username,
            "date_sent": self.date_sent.isoformat(),
            "title": self.title,
            "message": self.message,
            "redirectLink": self.redirectLink
        }