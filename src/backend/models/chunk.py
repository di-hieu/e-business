"""
SC Chatbot Knowledge Chunk Model

Vector chunk storage for RAG.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship


class KnowledgeChunk:
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
    
    def __init__(self, document_id: int, text: str, vector=None, metadata=None,
                 is_active: bool = True):
        self.document_id = document_id
        self.text = text
        self.vector = vector
        self.metadata = metadata
        self.is_active = is_active

    def to_dict(self):
        """Convert to dictionary."""
        return {
            "id": self.id,
            "document_id": self.document_id,
            "text": self.text,
            "vector": self.vector,
            "metadata": self.metadata,
            "is_active": self.is_active,
            "created_at": self.created_at
        }

    def __repr__(self):
        return f"<KnowledgeChunk(text='{self.text[:50]}...')>"