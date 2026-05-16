"""
SC Chatbot Knowledge Document Model

Knowledge base document storage for RAG.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, JSON
from sqlalchemy.orm import relationship


class KnowledgeDocument:
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
    
    def __init__(self, tenant_id: int, original_filename: str, content_type: str,
                 file_size: int = 0, parsed_content: str = None, metadata: str = None,
                 is_processed: bool = False, is_active: bool = True):
        self.tenant_id = tenant_id
        self.original_filename = original_filename
        self.content_type = content_type
        self.file_size = file_size
        self.parsed_content = parsed_content
        self.metadata = metadata
        self.is_processed = is_processed
        self.is_active = is_active

    def to_dict(self):
        """Convert to dictionary."""
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "original_filename": self.original_filename,
            "content_type": self.content_type,
            "file_size": self.file_size,
            "parsed_content": self.parsed_content,
            "chunk_count": self.chunk_count,
            "metadata": self.metadata,
            "is_processed": self.is_processed,
            "is_active": self.is_active,
            "uploaded_at": self.uploaded_at,
            "processed_at": self.processed_at,
            "updated_at": self.updated_at
        }

    def __repr__(self):
        return f"<KnowledgeDocument(filename='{self.original_filename}')>"


class KnowledgeBase:
    """Represents a knowledge base for a tenant."""

    __tablename__ = "knowledge_bases"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False)
    name = Column(String(255), nullable=False, comment="Knowledge base name")

    # Documents
    documents = relationship("KnowledgeDocument", back_populates="kb", cascade="all, delete-orphan")

    # Settings
    settings = Column(JSON, default=lambda: {}, nullable=True, comment="Knowledge base settings")

    # Timestamps
    created_at = Column(DateTime, default=lambda: __import__('datetime').datetime.utcnow())
    updated_at = Column(DateTime, default=lambda: __import__('datetime').datetime.utcnow(), onupdate=lambda: __import__('datetime').datetime.utcnow())

    def __init__(self, tenant_id: int, name: str, documents: list = None, settings: dict = None):
        self.tenant_id = tenant_id
        self.name = name
        self.documents = documents or []
        self.settings = settings or {}

    def to_dict(self):
        """Convert to dictionary."""
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "name": self.name,
            "documents": [d.to_dict() for d in self.documents],
            "settings": self.settings,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def __repr__(self):
        return f"<KnowledgeBase(id={self.id}, name='{self.name}')>"