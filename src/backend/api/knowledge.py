"""
SC Chatbot Knowledge Endpoints

Knowledge management API endpoints for uploading, storing, and managing
FAQs, product documentation, and policies.
"""

import sys
import os

# Add backend root to path for absolute imports
backend_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if backend_root not in sys.path:
    sys.path.insert(0, backend_root)

from fastapi import APIRouter, HTTPException, Depends, Request, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional
import hashlib

import models.database as db_model
import services.auth_service as auth_service
import models.knowledge as knowledge_model
import models.tenant as tenant_model

router = APIRouter(prefix="/knowledge", tags=["Knowledge"])


def get_current_user(request: Request):
    """Get current user from token."""
    token = auth_service.verify_token_from_header(request)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    
    return auth_service.verify_token(token)


class KnowledgeUploadRequest(BaseModel):
    """Knowledge upload request model."""
    content: str
    title: Optional[str] = None
    tenant_key: str


@router.post("/upload", response_model=dict)
async def upload_knowledge(
    file: Optional[UploadFile] = File(None),
    content: Optional[str] = Form(None),
    title: Optional[str] = Form(None),
    request: Request = None,
):
    """
    Upload knowledge document or content.
    
    Supports PDF, DOCX, TXT files, or plain text content.
    """
    token = auth_service.verify_token_from_header(request)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    
    user_info = auth_service.verify_token(token)
    
    # Get tenant
    async with db_model.get_db_session() as session:
        tenant = session.query("tenants").filter(
            "tenants.tenant_key = ?",
            [user_info.get("tenant_key")],
        ).first()
        
        if not tenant:
            raise HTTPException(status_code=404, detail="Tenant not found")
        
        # Handle file upload
        if file:
            filename = file.filename or f"document_{hashlib.md5(str(file.file).encode()).hexdigest()[:8]}.txt"
            
            # Store file content
            content = await file.read()
            content_text = content.decode("utf-8", errors="ignore")
            
            # Get existing knowledge or create new
            existing = session.query("knowledge").filter(
                "knowledge.tenant_id = ?",
                [tenant.id],
            ).first()
            
            if existing:
                # Update existing
                existing.content = content_text
                existing.title = title or existing.title
                existing.file_name = filename
            else:
                # Create new
                knowledge = knowledge_model.Knowledge(
                    tenant_id=tenant.id,
                    content=content_text,
                    title=title or f"Uploaded Knowledge",
                    file_name=filename,
                )
                session.add(knowledge)
            
            session.commit()
            
            return {
                "status": "success",
                "message": "Knowledge uploaded successfully",
                "knowledge_id": knowledge.id if knowledge else existing.id,
                "file_name": filename,
            }
        
        # Handle plain text content
        if content:
            existing = session.query("knowledge").filter(
                "knowledge.tenant_id = ?",
                [tenant.id],
            ).first()
            
            if existing:
                existing.content = content
                existing.title = title or existing.title
            else:
                knowledge = knowledge_model.Knowledge(
                    tenant_id=tenant.id,
                    content=content,
                    title=title or "Text Content",
                )
                session.add(knowledge)
            
            session.commit()
            
            return {
                "status": "success",
                "message": "Knowledge saved successfully",
                "knowledge_id": knowledge.id if knowledge else existing.id,
            }
        
        return {
            "status": "error",
            "message": "No content or file provided",
        }


@router.post("/update", response_model=dict)
async def update_knowledge(
    content: str = Form(...),
    title: Optional[str] = Form(None),
    knowledge_id: str = Form(None),
    request: Request = None,
):
    """
    Update existing knowledge content.
    """
    token = auth_service.verify_token_from_header(request)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    
    user_info = auth_service.verify_token(token)
    
    async with db_model.get_db_session() as session:
        knowledge = session.query("knowledge").filter(
            "knowledge.id = ?",
            [knowledge_id],
        ).first()
        
        if not knowledge:
            raise HTTPException(status_code=404, detail="Knowledge not found")
        
        knowledge.content = content
        knowledge.title = title or knowledge.title
        
        session.commit()
        
        return {
            "status": "success",
            "message": "Knowledge updated successfully",
        }


@router.post("/delete", response_model=dict)
async def delete_knowledge(
    knowledge_id: str = Form(...),
    request: Request = None,
):
    """
    Delete knowledge document.
    """
    token = auth_service.verify_token_from_header(request)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    
    user_info = auth_service.verify_token(token)
    
    async with db_model.get_db_session() as session:
        knowledge = session.query("knowledge").filter(
            "knowledge.id = ?",
            [knowledge_id],
        ).first()
        
        if not knowledge:
            raise HTTPException(status_code=404, detail="Knowledge not found")
        
        session.delete(knowledge)
        session.commit()
        
        return {
            "status": "success",
            "message": "Knowledge deleted successfully",
        }


@router.get("/list", response_model=dict)
async def list_knowledge(
    request: Request = None,
):
    """
    List all knowledge for the tenant.
    """
    token = auth_service.verify_token_from_header(request)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    
    user_info = auth_service.verify_token(token)
    
    async with db_model.get_db_session() as session:
        tenant = session.query("tenants").filter(
            "tenants.tenant_key = ?",
            [user_info.get("tenant_key")],
        ).first()
        
        if not tenant:
            raise HTTPException(status_code=404, detail="Tenant not found")
        
        knowledge_items = session.query("knowledge").filter(
            "knowledge.tenant_id = ?",
            [tenant.id],
        ).all()
        
        return {
            "knowledge": [
                {
                    "id": k.id,
                    "title": k.title,
                    "file_name": k.file_name,
                    "created_at": k.created_at,
                }
                for k in knowledge_items
            ]
        }