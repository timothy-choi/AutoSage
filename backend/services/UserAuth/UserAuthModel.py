from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from backend.resources.database import Base  

class UserAuth(Base):
    __tablename__ = 'user_auth'

    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    username = Column(String(50), unique=True, nullable=True)
    email = Column(String(250), unique=True, nullable=True)
    password = Column(String(300), nullable=True)
    hash_value = Column(String(300), nullable=True)
    is_verified = Column(Boolean, default=False)
    google_oauth = Column(JSONB, unique=True, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "hash_value": self.hash_value,
            "is_verified": self.is_verified,
            "google_oauth": self.google_oauth
        }