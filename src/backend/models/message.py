"""
SC Chatbot Message Model

Message storage for conversation history.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

from database import Base, get_db_session


class Message(Base):
    """Represents a chat message."""
    
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey('conversations.id'), nullable=False)
    
    # Message content
    role = Column(String(20), nullable=False, comment="user or assistant")
    content = Column(Text, nullable=True, comment="Message text content")
    
    # Channel-specific data (stored as JSONB)
    channel_data = Column(JSONB, nullable=True, comment="Zalo/FB/Instagram specific data")
    
    # Metadata
    is_tool_call = Column(Boolean, default=False)
    tool_call_id = Column(String(100), nullable=True)
    tool_name = Column(String(100), nullable=True)
    tool_result = Column(JSONB, nullable=True, comment="Tool execution result")
    
    # Token usage
    tokens_in = Column(Integer, default=0)
    tokens_out = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, server_default=Text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, onupdate=Text("CURRENT_TIMESTAMP"))
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")