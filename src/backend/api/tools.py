"""
SC Chatbot Tools Endpoints

Custom tool management API endpoints for defining and executing
business automation tools.
"""

import sys
import os

# Add backend root to path for absolute imports
backend_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if backend_root not in sys.path:
    sys.path.insert(0, backend_root)

from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from typing import Optional, Dict, Any

import models.database as db_model
import services.auth_service as auth_service
from services.tool_service import get_tools

router = APIRouter(prefix="/tools", tags=["Tools"])


def get_current_user(request: Request):
    """Get current user from token."""
    token = auth_service.verify_token_from_header(request)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    
    return auth_service.verify_token(token)


class ToolDefinition(BaseModel):
    """Tool definition model."""
    name: str
    description: str
    parameters: Dict[str, Any]
    endpoint: str
    method: str = "POST"


@router.post("/register", response_model=dict)
async def register_tool(
    data: ToolDefinition,
    request: Request = None,
):
    """
    Register a new custom tool.
    
    The tool will be available for the chatbot to call
    when appropriate.
    """
    # In POC mode, we store tools in memory
    # In production, you might want to use a database
    
    tool_info = {
        "name": data.name,
        "description": data.description,
        "parameters": data.parameters,
        "endpoint": data.endpoint,
        "method": data.method,
    }
    
    # Add to existing tools
    existing_tools = tool_service.get_tools()
    existing_tools.append(tool_info)
    tool_service.save_tools(existing_tools)
    
    return {
        "status": "success",
        "message": f"Tool {data.name} registered",
        "tool": tool_info,
    }


# Unregister a tool
def unregister_tool(name: str) -> dict:
    """Unregister a tool by name."""
    tools: list[dict] = get_tools()
    
    # Remove tool
    tools = [t for t in tools if t["name"] != name]
    save_tools(tools)
    
    return {
        "status": "success",
        "message": f"Tool {name} unregistered",
    }