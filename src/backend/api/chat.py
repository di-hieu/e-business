"""
SC Chatbot Chat Endpoints

Chat messaging API endpoints for the chatbot.
"""

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import json

from ..models.conversation import Conversation
from ..models.message import Message
from ..services.auth_service import AuthService
from ..rag.pipeline import RAGPipeline
from ..models.database import get_db_session

router = APIRouter(prefix="/chat", tags=["Chat"])


class ChatMessageRequest(BaseModel):
    """Chat message request model."""
    tenant_key: str
    user_message: str
    conversation_id: Optional[int] = None


class ChatMessageResponse(BaseModel):
    """Chat message response model."""
    success: bool
    message: Optional[str] = None
    conversation_id: Optional[int] = None
    tool_calls: Optional[List[dict]] = None
    tool_results: Optional[List[dict]] = None


@router.post("/message", response_model=ChatMessageResponse)
async def send_chat_message(
    request: ChatMessageRequest,
    token: str,
):
    """Send a message to the chatbot and get response."""
    
    # Verify token
    user_info = AuthService.verify_token(token)
    if not user_info:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # Verify tenant
    async with get_db_session() as session:
        tenant = session.query("tenants").filter(
            "tenants.tenant_key == ?",
        ).first()
    
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    # Create or get conversation
    conversation = await get_or_create_conversation(
        session=session,
        user_id=user_info["sub"],
        tenant_id=tenant.id,
        channel=request.conversation_id,
    )
    
    # Store user message
    user_message = Message(
        conversation_id=conversation.id,
        role="user",
        content=request.user_message,
    )
    session.add(user_message)
    session.commit()
    
    # Initialize RAG pipeline and get response
    rag_pipeline = RAGPipeline(tenant_id=tenant.id)
    response = await rag_pipeline.generate_response(request.user_message)
    
    # Create assistant message
    assistant_message = Message(
        conversation_id=conversation.id,
        role="assistant",
        content=response,
    )
    session.add(assistant_message)
    session.commit()
    
    return {
        "success": True,
        "message": response,
        "conversation_id": conversation.id,
    }


@router.websocket("/ws/{conversation_id}")
async def websocket_endpoint(conversation_id: int):
    """WebSocket endpoint for streaming chat messages."""
    
    # Verify user
    from ..services.auth_service import AuthService
    
    # Get user from WebSocket headers
    token = None  # Would extract from headers
    
    user_info = AuthService.verify_token(token)
    if not user_info:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    websocket = WebSocket.accept()
    await websocket.accept()
    
    # Handle streaming messages
    while True:
        data = await websocket.receive_text()
        
        if data == "ping":
            await websocket.send_text("pong")
        else:
            await websocket.send_text(json.dumps({
                "type": "message",
                "content": data,
            }))
    
    await websocket.close()


@router.get("/conversations")
async def list_conversations(
    user_id: str,
    limit: int = 20,
):
    """List user's conversations."""
    async with get_db_session() as session:
        conversations = session.query(Conversation).filter(
            Conversation.user_id == user_id,
            Conversation.is_active == True,
        ).order_by(Conversation.created_at.desc()).limit(limit).all()
        
        return [
            {
                "id": conv.id,
                "title": conv.title,
                "channel": conv.channel,
                "created_at": conv.created_at,
            }
            for conv in conversations
        ]