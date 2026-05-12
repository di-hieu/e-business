"""
SC Chatbot Tool Definition Model

Tool definition storage for function calling.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship

from database import Base, get_db_session


class ToolDefinition(Base):
    """Represents a custom tool definition."""
    
    __tablename__ = "tool_definitions"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False)
    
    # Tool metadata
    name = Column(String(100), nullable=False, comment="Tool name (e.g., check_inventory)")
    description = Column(Text, nullable=False, comment="Tool description for LLM")
    endpoint = Column(String(255), nullable=True, comment="API endpoint to call")
    method = Column(String(10), default="POST", comment="HTTP method")
    
    # JSON Schema parameters
    parameters_schema = Column(JSON, nullable=False, comment="JSON Schema for tool parameters")
    
    # Status
    is_active = Column(Boolean, default=True, comment="Whether tool is available")
    error_message = Column(Text, nullable=True, comment="Last error from endpoint")
    
    # Timestamps
    created_at = Column(DateTime, default=lambda: __import__('datetime').datetime.utcnow())
    updated_at = Column(DateTime, default=lambda: __import__('datetime').datetime.utcnow(), onupdate=lambda: __import__('datetime').datetime.utcnow())
    
    # Relationships
    tenant = relationship("Tenant", back_populates="tools")