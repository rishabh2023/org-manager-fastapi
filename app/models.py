from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.db import Base
import uuid, datetime

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    owner_user_id = Column(UUID(as_uuid=True), nullable=False)  # from Supabase Auth
