"""
SC Chatbot Knowledge Document Model

Knowledge base document storage for RAG.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship

from database import Base, get_db_session


class KnowledgeDocument(Base):
    """Represents a knowledge base document."""
    
    __tablename__ = "knowledge_documents"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False)
    
    # Document metadata
    original_filename = Column(String(255), nullable=False, comment="Original file name")
    content_type = Column(String(100), nullable=False, comment="text/plain, text/html, application/pdf")
    file_size = Column(Integer, comment="File size in bytes")
    
    # Document content (stored as text after parsing)
    parsed_content = Column(Text, nullable=True, comment="Parsed text content")
    
    # RAG metadata
    chunk_count = Column(Integer, default=0, comment="Number of chunks created")
    metadata = Column(String(255), nullable=True, comment="Document metadata")
    
    # Status
    is_processed = Column(Boolean, default=False, comment="Whether document has been processed")
    is_active = Column(Boolean, default=True, comment="Whether document should be used for retrieval")
    
    # Timestamps
    uploaded_at = Column(DateTime, default=lambda: __import__('datetime').datetime.utcnow())
    processed_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=lambda: __import__('datetime').datetime.utcnow(), onupdate=lambda: __import__('datetime').datetime.utcnow())
    
    # Relationships
    tenant = relationship("Tenant", back_populates="knowledge_docs")
    chunks = relationship("KnowledgeChunk", back_populates="document", cascade="all, delete-orphan")