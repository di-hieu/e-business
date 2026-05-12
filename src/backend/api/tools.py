"""
SC Chatbot Tool Endpoints

Tool definition and execution API endpoints.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

from ..models.tool import ToolDefinition
from ..models.database import get_db_session

router = APIRouter(prefix="/tools", tags=["Tools"])


class ToolDefinitionResponse(BaseModel):
    """Tool definition response model."""
    id: int
    name: str
    description: str
    parameters: dict
    endpoint: Optional[str]
    method: str
    is_active: bool
    created_at: str
    updated_at: str


class ToolRequest(BaseModel):
    """Tool execution request model."""
    tool_name: str
    parameters: Dict[str, Any]


class ToolResponse(BaseModel):
    """Tool execution response model."""
    success: bool
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


@router.get("/definitions", response_model=List[ToolDefinitionResponse])
async def get_tool_definitions(
    tenant_key: str,
    api_key: str,
):
    """Get all tool definitions for tenant."""
    
    if not tenant_key or not api_key:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    async with get_db_session() as session:
        tools = session.query(ToolDefinition).filter(
            ToolDefinition.tenant_id == tenant_key,
            ToolDefinition.is_active == True,
        ).all()
        
        return [
            {
                "id": tool.id,
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters_schema,
                "endpoint": tool.endpoint,
                "method": tool.method,
                "is_active": tool.is_active,
                "created_at": tool.created_at,
                "updated_at": tool.updated_at,
            }
            for tool in tools
        ]


@router.post("/execute", response_model=ToolResponse)
async def execute_tool(
    request: ToolRequest,
    tenant_key: str,
    api_key: str,
):
    """Execute a tool with given parameters."""
    
    if not tenant_key or not api_key:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    async with get_db_session() as session:
        # Get tool definition
        tool = session.query(ToolDefinition).filter(
            ToolDefinition.tenant_id == tenant_key,
            ToolDefinition.name == request.tool_name,
            ToolDefinition.is_active == True,
        ).first()
        
        if not tool:
            return {
                "success": False,
                "error": f"Tool '{request.tool_name}' not found",
            }
        
        # Call the endpoint
        import httpx
        
        params = tool.parameters_schema.get("properties", {})
        payload = {
            k: v for k, v in request.parameters.items() if k in params
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.request(
                    tool.method.lower() if tool.method else "POST",
                    tool.endpoint or "http://localhost:8000/api",
                    json=payload,
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                    },
                )
                
                return {
                    "success": response.status_code < 400,
                    "result": response.json() if response.content else {},
                    "error": None,
                }
        except Exception as e:
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }


@router.post("/define", response_model=ToolDefinitionResponse)
async def define_tool(
    name: str,
    description: str,
    parameters: dict,
    endpoint: Optional[str] = None,
    method: str = "POST",
    is_active: bool = True,
    tenant_key: str = None,
    api_key: str = None,
):
    """Define a new tool for tenant."""
    
    if not tenant_key or not api_key:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    async with get_db_session() as session:
        # Check if tool already exists
        existing = session.query(ToolDefinition).filter(
            ToolDefinition.tenant_id == tenant_key,
            ToolDefinition.name == name,
        ).first()
        
        if existing:
            return {
                "id": existing.id,
                "name": existing.name,
                "description": existing.description,
                "parameters": existing.parameters_schema,
                "endpoint": existing.endpoint,
                "method": existing.method,
                "is_active": existing.is_active,
                "created_at": existing.created_at,
                "updated_at": existing.updated_at,
            }
        
        # Create tool definition
        tool = ToolDefinition(
            tenant_id=tenant_key,
            name=name,
            description=description,
            parameters_schema=parameters,
            endpoint=endpoint,
            method=method,
            is_active=is_active,
        )
        
        session.add(tool)
        session.commit()
        
        return {
            "id": tool.id,
            "name": tool.name,
            "description": tool.description,
            "parameters": tool.parameters_schema,
            "endpoint": tool.endpoint,
            "method": tool.method,
            "is_active": tool.is_active,
            "created_at": tool.created_at,
            "updated_at": tool.updated_at,
        }


@router.delete("/{tool_id}")
async def delete_tool(
    tool_id: int,
    tenant_key: str,
    api_key: str,
):
    """Delete a tool definition."""
    
    if not tenant_key or not api_key:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    async with get_db_session() as session:
        tool = session.query(ToolDefinition).filter(
            ToolDefinition.id == tool_id,
            ToolDefinition.tenant_id == tenant_key,
        ).first()
        
        if not tool:
            raise HTTPException(status_code=404, detail="Tool not found")
        
        session.delete(tool)
        session.commit()
        
        return {"success": True, "message": "Tool deleted"}


@router.put("/{tool_id}/active")
async def toggle_tool_active(
    tool_id: int,
    is_active: bool,
    tenant_key: str,
    api_key: str,
):
    """Toggle tool active status."""
    
    if not tenant_key or not api_key:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    async with get_db_session() as session:
        tool = session.query(ToolDefinition).filter(
            ToolDefinition.id == tool_id,
            ToolDefinition.tenant_id == tenant_key,
        ).first()
        
        if not tool:
            raise HTTPException(status_code=404, detail="Tool not found")
        
        tool.is_active = is_active
        session.commit()
        
        return {
            "success": True,
            "is_active": tool.is_active,
        }