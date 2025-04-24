from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone
import uuid

Base = declarative_base()

class UserWorkflowInfo(Base):
    __tablename__ = "user_workflow_info"

    id = Column(PG_UUID(as_uuid=True), primary_key=True)
    user_id = Column(PG_UUID(as_uuid=True))
    env_variables = Column(JSON, nullable=True)
    stored_keys = Column(ARRAY(JSON), nullable=True)
    user_credentials = Column(ARRAY(JSON), nullable=True)
    websites = Column(ARRAY(JSON), nullable=True)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "env_variables": self.env_variables,
            "stored_keys": self.stored_keys,
            "user_credentials": self.user_credentials,
            "websites": self.websites,
            "updated_at": self.updated_at
        }