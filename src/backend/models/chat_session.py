"""
SC Chatbot Chat Session Model

Chat session for managing LLM state.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship

from database import Base, get_db_session


class ChatSession(Base):
    """Represents a chat session with state and history."""
    
    __tablename__ = "chat_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey('conversations.id'), nullable=False)
    
    # Session state
    state = Column(JSON, default=lambda: {}, nullable=False, comment="Session state for LangGraph")
    history = Column(JSON, nullable=True, comment="Conversation history")
    
    # Metadata
    model_name = Column(String(50), nullable=True, comment="LLM model used")
    temperature = Column(Float, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=lambda: __import__('datetime').datetime.utcnow())
    updated_at = Column(DateTime, default=lambda: __import__('datetime').datetime.utcnow(), onupdate=lambda: __import__('datetime').datetime.utcnow())
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")