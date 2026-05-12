"""
SC Chatbot User Model

User authentication and authorization model.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from enum import Enum as SQLEnum

from database import Base, get_db_session


class UserRole(SQLEnum):
    """User roles for RBAC."""
    ADMIN = "admin"
    TENANT_ADMIN = "tenant_admin"
    AGENT = "agent"


class User(Base):
    """Represents a user within a tenant."""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False, comment="User email")
    hashed_password = Column(String(255), nullable=False, comment="Bcrypt hashed password")
    
    # Role and permissions
    role = Column(Enum(UserRole), default=UserRole.AGENT, nullable=False)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="users", foreign_keys=[tenant_id])
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")
    chat_sessions = relationship("ChatSession", back_populates="user", cascade="all, delete-orphan")
    
    # Timestamps
    created_at = Column(DateTime, default=lambda: __import__('datetime').datetime.utcnow())
    updated_at = Column(DateTime, default=lambda: __import__('datetime').datetime.utcnow(), onupdate=lambda: __import__('datetime').datetime.utcnow())
    
    # Tenant foreign key (for proper relation)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False)