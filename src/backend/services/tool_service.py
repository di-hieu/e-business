"""
SC Chatbot Tool Service

Tool calling service for function execution.
"""

from typing import Dict, Any, List
from datetime import datetime
import httpx

from ..models.tool import ToolDefinition


class ToolService:
    """Service for managing tool calls."""
    
    def __init__(self, tenant_id: int):
        """Initialize tool service."""
        self.tenant_id = tenant_id
    
    async def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """Get all active tool definitions for tenant."""
        from ..models.database import get_db_session
        
        async with get_db_session() as session:
            tools = session.query(ToolDefinition).filter(
                ToolDefinition.tenant_id == self.tenant_id,
                ToolDefinition.is_active == True,
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
        from ..models.database import get_db_session
        
        async with get_db_session() as session:
            tool = session.query(ToolDefinition).filter(
                ToolDefinition.tenant_id == self.tenant_id,
                ToolDefinition.name == tool_name,
                ToolDefinition.is_active == True,
            ).first()
            
            if not tool:
                return {
                    "success": False,
                    "error": f"Tool '{tool_name}' not found",
                }
            
            # Call the endpoint
            headers = {
                "Authorization": f"Bearer {tool.tenant.api_key}",
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