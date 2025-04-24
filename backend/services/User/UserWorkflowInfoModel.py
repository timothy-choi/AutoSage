from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone
import uuid

Base = declarative_base()

class UserWorkflowInfo(Base):
    __tablename__ = "user_workflow_info"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True),  ForeignKey("users.id"), nullable=False)
    env_variables = Column(JSON, nullable=True)
    stored_keys = Column(JSON, nullable=True)
    user_credentials = Column(JSON, nullable=True)
    websites = Column(JSON, nullable=True)
    apps = Column(JSON, nullable=True)
    file_paths = Column(JSON, nullable=True)
    container_images = Column(JSON, nullable=True)
    workflow_preferences = Column(JSON, nullable=True)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "env_variables": self.env_variables,
            "stored_keys": self.stored_keys,
            "user_credentials": self.user_credentials,
            "websites": self.websites,
            "apps": self.apps,
            "file_paths": self.file_paths,
            "container_images": self.container_images,
            "workflow_preferences": self.workflow_preferences,
            "updated_at": self.updated_at
        }