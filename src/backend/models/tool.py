"""
SC Chatbot Tool Definition Model

Tool definition storage for function calling.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship


class ToolDefinition:
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
    
    def __init__(self, tenant_id: int, name: str, description: str,
                 endpoint: str = None, method: str = "POST", parameters_schema=None,
                 is_active: bool = True, error_message=None):
        self.tenant_id = tenant_id
        self.name = name
        self.description = description
        self.endpoint = endpoint
        self.method = method
        self.parameters_schema = parameters_schema
        self.is_active = is_active
        self.error_message = error_message

    def to_dict(self):
        """Convert to dictionary."""
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "name": self.name,
            "description": self.description,
            "endpoint": self.endpoint,
            "method": self.method,
            "parameters_schema": self.parameters_schema,
            "is_active": self.is_active,
            "error_message": self.error_message,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def __repr__(self):
        return f"<ToolDefinition(name='{self.name}')>"


class Tool:
    """Represents a tool instance (execution result)."""

    __tablename__ = "tools"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey('tool_definitions.id'), nullable=False)
    tool_definition_id = Column(Integer, ForeignKey('tool_definitions.id'), nullable=False)

    # Execution result
    result = Column(JSON, nullable=True, comment="Tool execution result")
    error = Column(Text, nullable=True, comment="Tool execution error")

    # Status
    is_executed = Column(Boolean, default=False, comment="Whether tool has been executed")
    last_executed_at = Column(DateTime, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=lambda: __import__('datetime').datetime.utcnow())
    executed_at = Column(DateTime, default=lambda: __import__('datetime').datetime.utcnow(), onupdate=lambda: __import__('datetime').datetime.utcnow())

    def __init__(self, tenant_id: int, tool_definition_id: int, result: dict = None, error: str = None):
        self.tenant_id = tenant_id
        self.tool_definition_id = tool_definition_id
        self.result = result
        self.error = error

    def to_dict(self):
        """Convert to dictionary."""
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "tool_definition_id": self.tool_definition_id,
            "result": self.result,
            "error": self.error,
            "is_executed": self.is_executed,
            "last_executed_at": self.last_executed_at,
            "created_at": self.created_at,
            "executed_at": self.executed_at
        }

    def __repr__(self):
        return f"<Tool(id={self.id}, tool_definition_id={self.tool_definition_id})>"