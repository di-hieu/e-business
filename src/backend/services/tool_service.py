"""
SC Chatbot Tool Service

Tool calling service for function execution.
"""

import sys
import os

# Add backend root to path for absolute imports
backend_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if backend_root not in sys.path:
    sys.path.insert(0, backend_root)

from typing import Dict, Any, List
from datetime import datetime
import httpx

import models.tool as tool_model


class ToolService:
    """Service for managing tool calls."""
    
    def __init__(self, tenant_id: int):
        """Initialize tool service."""
        self.tenant_id = tenant_id
    
    async def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """Get all active tool definitions for tenant."""
        from models.database import get_db_session
        
        async with get_db_session() as session:
            tools = session.query("ToolDefinition").filter(
                "ToolDefinition.tenant_id = ? AND ToolDefinition.is_active",
                [self.tenant_id],
            ).all()
            
            return [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters_schema,
                    "endpoint": tool.endpoint,
                    "method": tool.method,
                }
                for tool in tools
            ]
    
    async def call_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Call a tool with given parameters."""
        from models.database import get_db_session
        
        async with get_db_session() as session:
            tool = session.query("ToolDefinition").filter(
                "ToolDefinition.tenant_id = ? AND ToolDefinition.name = ? AND ToolDefinition.is_active",
                [self.tenant_id, tool_name],
            ).first()
            
            if not tool:
                return {
                    "success": False,
                    "error": f"Tool '{tool_name}' not found",
                }
            
            # Call the endpoint
            headers = {
                "Authorization": f"Bearer {tool.api_key}",
                "Content-Type": "application/json",
            }
            
            params = tool.parameters_schema.get("properties", {})
            payload = {
                k: v for k, v in parameters.items() if k in params
            }
            
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.request(
                        tool.method.lower() if tool.method else "POST",
                        tool.endpoint or "http://localhost:8000/api",
                        json=payload,
                        headers=headers,
                    )
                    
                    return {
                        "success": response.status_code < 400,
                        "result": response.json() if response.content else {},
                        "status_code": response.status_code,
                    }
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e),
                }


# Global tools storage (for POC mode)
_tools_cache: List[Dict[str, Any]] = []


def get_tools() -> List[Dict[str, Any]]:
    """Get all registered tools from cache."""
    return _tools_cache


def save_tools(tools: List[Dict[str, Any]]):
    """Save tools to cache."""
    _tools_cache = tools


def register_tool(name: str, description: str, parameters: Dict[str, Any], endpoint: str, method: str = "POST"):
    """Register a tool (for POC mode)."""
    tools = get_tools()
    tools.append({
        "name": name,
        "description": description,
        "parameters": parameters,
        "endpoint": endpoint,
        "method": method,
    })
    save_tools(tools)