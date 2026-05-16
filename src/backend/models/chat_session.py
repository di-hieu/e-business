"""
SC Chatbot Chat Session Model

Chat session for managing LLM state.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON, Float
from sqlalchemy.orm import relationship


class ChatSession:
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
    
    def __init__(self, conversation_id: int, state: dict = None, model_name: str = None,
                 temperature: float = None):
        self.conversation_id = conversation_id
        self.state = state or {}
        self.model_name = model_name
        self.temperature = temperature

    def to_dict(self):
        """Convert to dictionary."""
        return {
            "id": self.id,
            "conversation_id": self.conversation_id,
            "state": self.state,
            "history": self.history,
            "model_name": self.model_name,
            "temperature": self.temperature,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def __repr__(self):
        return f"<ChatSession(conversation_id={self.conversation_id})>"