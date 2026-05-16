"""
SC Chatbot Chat Endpoints

Chat messaging and conversation management API endpoints.
"""

import sys
import os

# Add backend root to path for absolute imports
backend_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if backend_root not in sys.path:
    sys.path.insert(0, backend_root)

from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from typing import Optional
import uuid

import models.database as db_model
import services.auth_service as auth_service
import models.conversation as conversation_model
import models.message as message_model
import rag.pipeline as rag_pipeline
from services.tool_service import get_tools

router = APIRouter(prefix="/api/chat", tags=["Chat"])


def get_current_user(request: Request):
    """Get current user from token."""
    token = auth_service.verify_token_from_header(request)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    
    return auth_service.verify_token(token)


@router.post("/message", response_model=dict)
async def send_message(
    request: Request,
    message: dict,
    token: str = Depends(get_current_user),
):
    """
    Send a message to the chatbot.
    
    The chatbot will respond using RAG (Retrieval-Augmented Generation)
    and may call custom tools if needed.
    """
    user_info = auth_service.verify_token(token)
    
    # Get or create conversation
    async with db_model.get_db_session() as session:
        # Find tenant for this user
        tenant = session.query("tenants").filter(
            "tenants.tenant_key = ?",
            [user_info.get("tenant_key")],
        ).first()
        
        if not tenant:
            raise HTTPException(status_code=404, detail="Tenant not found")
        
        # Create or get conversation
        user_id = str(user_info.get("sub", user_info.get("id")))
        conversation = await conversation_model.get_or_create_conversation(
            session=session,
            user_id=user_id,
            tenant_id=tenant.id,
            channel="web",
        )
        
        # Store user message
        user_message = message_model.Message(
            conversation_id=conversation.id,
            role="user",
            content=message.get("content"),
        )
        session.add(user_message)
        session.commit()
        
        # Process with RAG pipeline
        rag = rag_pipeline.RAGPipeline(tenant_id=tenant.id)
        response = await rag.generate_response(message.get("content"))
        
        # Create assistant message
        assistant_message = message_model.Message(
            conversation_id=conversation.id,
            role="assistant",
            content=response,
        )
        session.add(assistant_message)
        session.commit()
        
        # Check if tools were called
        if isinstance(response, dict):
            if "error" in response and response["error"]:
                return response
            return {
                "status": "success",
                "response": response.get("response"),
                "conversation_id": conversation.id,
            }
        
        return {
            "status": "success",
            "response": response,
            "conversation_id": conversation.id,
        }


@router.post("/conversations", response_model=dict)
async def list_conversations(
    request: Request,
    token: str = Depends(get_current_user),
):
    """List all conversations for the current user."""
    user_info = auth_service.verify_token(token)
    
    async with db_model.get_db_session() as session:
        conversations = session.query("conversations").filter(
            "conversations.user_id = ?",
            [user_info.get("sub")],
        ).all()
        
        return {
            "conversations": [
                {
                    "id": conv.id,
                    "user_id": conv.user_id,
                    "tenant_id": conv.tenant_id,
                    "channel": conv.channel,
                }
                for conv in conversations
            ]
        }


@router.post("/conversations/{conv_id}", response_model=dict)
async def get_conversation(
    request: Request,
    conv_id: str,
    token: str = Depends(get_current_user),
):
    """Get details of a specific conversation."""
    user_info = auth_service.verify_token(token)
    
    async with db_model.get_db_session() as session:
        conversation = session.query("conversations").filter(
            "conversations.id = ?",
            [conv_id],
        ).first()
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        return {
            "id": conversation.id,
            "user_id": conversation.user_id,
            "tenant_id": conversation.tenant_id,
            "channel": conversation.channel,
        }