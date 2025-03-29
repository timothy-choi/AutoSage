from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
from backend.resources.database import Base
from datetime import datetime, timezone

class User(Base):
    __tablename__ = "user"

    id = Column(PG_UUID(as_uuid=True), primary_key=True)
    name = Column(String(100), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    date_joined = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    userAuth_id = Column(PG_UUID(as_uuid=True), ForeignKey('user_auth.id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "email": self.email,
            "date_joined": self.date_joined,
            "userAuth_id": self.userAuth_id
        }
