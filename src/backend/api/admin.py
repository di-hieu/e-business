"""
SC Chatbot Admin Endpoints

Admin dashboard and management API endpoints.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from ..models.tenant import Tenant
from ..models.user import User
from ..models.conversation import Conversation
from ..models.message import Message
from ..models.knowledge import KnowledgeDocument
from ..models.tool import ToolDefinition
from ..services.auth_service import AuthService
from ..models.database import get_db_session

router = APIRouter(prefix="/admin", tags=["Admin"])


class AnalyticsResponse(BaseModel):
    """Analytics response model."""
    total_messages: int
    active_conversations: int
    avg_response_time_ms: float
    tool_calls: int
    errors: int


@router.get("/analytics")
async def get_analytics(
    tenant_key: str,
    api_key: str,
):
    """Get analytics dashboard data."""
    
    async with get_db_session() as session:
        tenant = session.query(Tenant).filter(
            Tenant.tenant_key == tenant_key,
        ).first()
        
        if not tenant:
            raise HTTPException(status_code=404, detail="Tenant not found")
        
        # Get conversation stats
        conversations = session.query(Conversation).filter(
            Conversation.tenant_id == tenant.id,
        ).all()
        
        messages = session.query(Message).filter(
            Message.conversation_id.in_([c.id for c in conversations]),
        ).all()
        
        # Calculate averages
        total_messages = len(messages)
        avg_response_time = 0.0
        tool_calls = 0
        errors = 0
        
        for msg in messages:
            if msg.is_tool_call:
                tool_calls += 1
            if msg.tool_result and msg.tool_result.get("error"):
                errors += 1
        
        return AnalyticsResponse(
            total_messages=total_messages,
            active_conversations=len(conversations),
            avg_response_time_ms=avg_response_time,
            tool_calls=tool_calls,
            errors=errors,
        )


@router.get("/users", response_model=List[dict])
async def list_users(
    tenant_key: str,
    api_key: str,
):
    """List all users for tenant."""
    
    async with get_db_session() as session:
        users = session.query(User).filter(
            User.tenant_id == tenant_key,
        ).all()
        
        return [
            {
                "id": str(u.id),
                "email": u.email,
                "role": u.role.value,
                "created_at": u.created_at,
            }
            for u in users
        ]


@router.get("/tenants")
async def list_tenants() -> List[dict]:
    """List all tenants (super admin only)."""
    
    async with get_db_session() as session:
        tenants = session.query(Tenant).all()
        
        return [
            {
                "id": str(t.id),
                "tenant_key": t.tenant_key,
                "name": t.name,
                "created_at": t.created_at,
            }
            for t in tenants
        ]


@router.get("/documents", response_model=List[dict])
async def list_documents(
    tenant_key: str,
    api_key: str,
):
    """List all knowledge documents."""
    
    async with get_db_session() as session:
        docs = session.query(KnowledgeDocument).filter(
            KnowledgeDocument.tenant_id == tenant_key,
        ).all()
        
        return [
            {
                "id": d.id,
                "filename": d.original_filename,
                "file_size": d.file_size,
                "chunk_count": d.chunk_count,
                "is_processed": d.is_processed,
                "is_active": d.is_active,
                "uploaded_at": d.uploaded_at,
            }
            for d in docs
        ]


@router.get("/tools", response_model=List[dict])
async def list_tools(
    tenant_key: str,
    api_key: str,
):
    """List all tool definitions."""
    
    async with get_db_session() as session:
        tools = session.query(ToolDefinition).filter(
            ToolDefinition.tenant_id == tenant_key,
        ).all()
        
        return [
            {
                "id": t.id,
                "name": t.name,
                "description": t.description,
                "is_active": t.is_active,
                "created_at": t.created_at,
            }
            for t in tools
        ]


@router.get("/conversations", response_model=List[dict])
async def list_conversations(
    tenant_key: str,
    api_key: str,
):
    """List all conversations with message count."""
    
    async with get_db_session() as session:
        conversations = session.query(Conversation).filter(
            Conversation.tenant_id == tenant_key,
        ).all()
        
        return [
            {
                "id": c.id,
                "title": c.title,
                "channel": c.channel,
                "user_id": c.user_id,
                "message_count": len(c.messages),
                "created_at": c.created_at,
            }
            for c in conversations
        ]


@router.get("/settings")
async def get_settings(
    tenant_key: str,
    api_key: str,
):
    """Get tenant settings."""
    
    async with get_db_session() as session:
        tenant = session.query(Tenant).filter(
            Tenant.tenant_key == tenant_key,
        ).first()
        
        return {
            "tenant_key": tenant.tenant_key,
            "model_name": tenant.model_name if tenant else None,
            "language": tenant.language if tenant else None,
        }


@router.post("/settings")
async def update_settings(
    model_name: Optional[str] = None,
    language: Optional[str] = None,
    response_style: Optional[str] = None,
    tenant_key: str = None,
    api_key: str = None,
):
    """Update tenant settings."""
    
    if not tenant_key or not api_key:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    async with get_db_session() as session:
        tenant = session.query(Tenant).filter(
            Tenant.tenant_key == tenant_key,
        ).first()
        
        if not tenant:
            raise HTTPException(status_code=404, detail="Tenant not found")
        
        if model_name:
            tenant.model_name = model_name
        if language:
            tenant.language = language
        if response_style:
            tenant.response_style = response_style
        
        session.commit()
        
        return {"success": True, "message": "Settings updated"}