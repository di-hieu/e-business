"""
SC Chatbot Conversation Model

Conversation management model.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship


class Conversation:
    """Represents a conversation in a chat session."""
    
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False)
    title = Column(String(255), default="", comment="Conversation title")
    
    # Relationships
    tenant = relationship("Tenant", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
    
    def __init__(self, tenant_id: int, title: str = ""):
        self.tenant_id = tenant_id
        self.title = title

    def to_dict(self):
        """Convert to dictionary."""
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "title": self.title
        }

    def __repr__(self):
        return f"<Conversation(title='{self.title}')>"