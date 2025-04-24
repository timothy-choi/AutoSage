from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
from backend.resources.database import Base
from datetime import datetime, timezone
import enum

class AccountPlans(enum.Enum):
    FREE = 'free'
    PRO = 'pro'
    ENTERPRISE = 'enterprise'

class User(Base):
    __tablename__ = "user"

    id = Column(PG_UUID(as_uuid=True), primary_key=True)
    name = Column(String(100), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    date_joined = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    userAuth_id = Column(PG_UUID(as_uuid=True), ForeignKey('user_auth.id'), nullable=False)
    is_active = Column(Boolean, nullable=True)
    last_login = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    last_login_ip = Column(String(100), nullable=False)
    notification_manager_id = Column(PG_UUID(as_uuid=True))
    account_plan = Column(Enum(AccountPlans), default='free')
    user_workflow_info_id = Column(PG_UUID(as_uuid=True))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "email": self.email,
            "date_joined": self.date_joined,
            "userAuth_id": self.userAuth_id,
            "is_active": self.is_active,
            "last_login": self.last_login,
            "last_login_ip": self.last_login_ip,
            "notification_manager_id": self.notification_manager_id,
            "account_plan": self.account_plan,
            "user_workflow_info_id": self.user_workflow_info_id
        }
