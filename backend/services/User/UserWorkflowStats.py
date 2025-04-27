from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, JSON, Integer
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone
import uuid

Base = declarative_base()

class UserWorkflowStats(Base):
    __tablename__ = "user_workflow_stats"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.id"), unique=True)

    total_workflows_created = Column(Integer, default=0)
    total_workflow_executions = Column(Integer, default=0)
    successful_executions = Column(Integer, default=0)
    failed_executions = Column(Integer, default=0)

    api_calls_made = Column(Integer, default=0)
    active_workflows = Column(Integer, default=0)

    most_used_workflow = Column(String(100), nullable=True)

    most_consistent_workflow = Column(String(100), nullable=True)
    least_consistent_workflow = Column(String(100), nullable=True)

    least_used_workflow = Column(String(100), nullable=True)

    workflow_activity_history = Column(ARRAY(JSON), nullable=True)

    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "total_workflows_created": self.total_workflows_created,
            "total_workflow_executions": self.total_workflow_executions,
            "successful_executions": self.successful_executions,
            "failed_executions": self.failed_executions,
            "api_calls_made": self.api_calls_made,
            "active_workflows": self.active_workflows,
            "most_used_workflow": self.most_used_workflow,
            "most_consistent_workflow": self.most_consistent_workflow,
            "least_consistent_workflow": self.least_consistent_workflow,
            "least_used_workflow": self.least_used_workflow,
            "workflow_activity_history": self.workflow_activity_history,
            "updated_at": self.updated_at
        }