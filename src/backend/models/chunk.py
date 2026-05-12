"""
SC Chatbot Knowledge Chunk Model

Vector chunk storage for RAG.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship

from database import Base, get_db_session


class KnowledgeChunk(Base):
    """Represents a vector chunk from a knowledge document."""
    
    __tablename__ = "knowledge_chunks"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey('knowledge_documents.id'), nullable=False)
    
    # Chunk content
    text = Column(Text, nullable=False, comment="Chunk text for embeddings")
    vector = Column(JSON, nullable=False, comment="Embedding vector")
    
    # Metadata for filtering
    metadata = Column(JSON, nullable=False, comment="Chunk metadata")
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=lambda: __import__('datetime').datetime.utcnow())
    
    # Relationships
    document = relationship("KnowledgeDocument", back_populates="chunks")