"""
SC Chatbot Message Model

Message storage for conversation history.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB


class Message:
    """Represents a chat message."""
    
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey('conversations.id'), nullable=False)
    
    # Message content
    role = Column(String(20), nullable=False, comment="user or assistant")
    content = Column(Text, nullable=True, comment="Message text content")
    
    # Channel-specific data (stored as JSONB)
    channel_data = Column(JSONB, nullable=True, comment="Zalo/FB/Instagram specific data")
    
    # Token usage
    tokens_in = Column(Integer, default=0)
    tokens_out = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, server_default="CURRENT_TIMESTAMP")
    updated_at = Column(DateTime, onupdate="CURRENT_TIMESTAMP")
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
    
    def __init__(self, conversation_id: int, role: str, content: str,
                 tokens_in: int = 0, tokens_out: int = 0, channel_data=None):
        self.conversation_id = conversation_id
        self.role = role
        self.content = content
        self.tokens_in = tokens_in
        self.tokens_out = tokens_out
        self.channel_data = channel_data

    def to_dict(self):
        """Convert to dictionary."""
        return {
            "id": self.id,
            "conversation_id": self.conversation_id,
            "role": self.role,
            "content": self.content,
            "tokens_in": self.tokens_in,
            "tokens_out": self.tokens_out,
            "channel_data": self.channel_data,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def __repr__(self):
        return f"<Message(role='{self.role}', content='{self.content[:50]}...')>"