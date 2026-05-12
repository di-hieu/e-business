"""
SC Chatbot Tenant Model

Multi-tenant isolation model.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, Text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from database import Base, get_db_session


class Tenant(Base):
    """Represents a multi-tenant workspace."""
    
    __tablename__ = "tenants"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_key = Column(String(50), unique=True, index=True, comment="Unique tenant identifier")
    name = Column(String(100), nullable=False, comment="Tenant/company name")
    api_key = Column(String(255), unique=True, nullable=False, comment="Tenant API key")
    
    # Settings
    llm_model = Column(String(50), default="gpt-4o-mini", comment="LLM model to use")
    response_style = Column(String(50), default="professional", comment="Response style: professional, casual, friendly")
    language = Column(String(10), default="en", comment="Default language code")
    
    # Quota management
    token_limit = Column(Integer, default=1000, comment="Monthly token limit")
    message_limit = Column(Integer, default=100, comment="Daily message limit")
    is_active = Column(Boolean, default=True, comment="Tenant status")
    
    # Timestamps
    created_at = Column(DateTime, default=lambda: __import__('datetime').datetime.utcnow())
    updated_at = Column(DateTime, default=lambda: __import__('datetime').datetime.utcnow(), onupdate=lambda: __import__('datetime').datetime.utcnow())
    
    # Relationships
    users = relationship("User", back_populates="tenant", cascade="all, delete-orphan")
    conversations = relationship("Conversation", back_populates="tenant", cascade="all, delete-orphan")
    knowledge_docs = relationship("KnowledgeDocument", back_populates="tenant", cascade="all, delete-orphan")
    tools = relationship("ToolDefinition", back_populates="tenant", cascade="all, delete-orphan")
    chat_sessions = relationship("ChatSession", back_populates="tenant", cascade="all, delete-orphan")