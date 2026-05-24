from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, Boolean
from sqlalchemy.sql import func
from app.database import Base
import enum


class ProjectStatus(str, enum.Enum):
    in_progress = "in_progress"
    completed   = "completed"
    industrial  = "industrial"


class Project(Base):
    __tablename__ = "projects"

    id           = Column(Integer, primary_key=True, index=True)
    title        = Column(String(200), nullable=False)
    description  = Column(Text, nullable=False)
    status       = Column(Enum(ProjectStatus), nullable=False)
    before_image = Column(String(500), nullable=True)
    after_image  = Column(String(500), nullable=True)
    created_at   = Column(DateTime(timezone=True), server_default=func.now())
    updated_at   = Column(DateTime(timezone=True), onupdate=func.now())


class QuoteRequest(Base):
    __tablename__ = "quote_requests"

    id           = Column(Integer, primary_key=True, index=True)
    full_name    = Column(String(200), nullable=False)
    email        = Column(String(200), nullable=False)
    phone        = Column(String(50),  nullable=True)
    company      = Column(String(200), nullable=True)
    project_type = Column(String(200), nullable=True)
    message      = Column(Text, nullable=False)
    is_read      = Column(Boolean, default=False)
    created_at   = Column(DateTime(timezone=True), server_default=func.now())


class AdminUser(Base):
    __tablename__ = "admin_users"

    id              = Column(Integer, primary_key=True, index=True)
    username        = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(256), nullable=False)
    created_at      = Column(DateTime(timezone=True), server_default=func.now())
