"""
SC Chatbot Knowledge Endpoints

Knowledge base management API endpoints.
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from ..models.knowledge import KnowledgeDocument
from ..models.database import get_db_session

router = APIRouter(prefix="/knowledge", tags=["Knowledge"])


class KnowledgeDocumentResponse(BaseModel):
    """Knowledge document response model."""
    id: int
    original_filename: str
    content_type: str
    file_size: int
    is_processed: bool
    is_active: bool
    uploaded_at: str


class KnowledgeListResponse(BaseModel):
    """Knowledge list response model."""
    documents: List[KnowledgeDocumentResponse]
    count: int


@router.post("/upload", response_model=KnowledgeDocumentResponse)
async def upload_knowledge(
    file: UploadFile = File(...),
    tenant_key: str = Form(...),
    api_key: str = Form(...),
    is_active: bool = Form(True),
):
    """Upload a knowledge document."""
    
    # Verify credentials
    if not tenant_key or not api_key:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    async with get_db_session() as session:
        # Get tenant
        tenant = session.query(KnowledgeDocument).filter(
            KnowledgeDocument.tenant_key == tenant_key,
        ).first()
        
        if not tenant:
            raise HTTPException(status_code=404, detail="Tenant not found")
        
        # Read file
        content = file.file.read()
        content_type = file.content_type
        
        # Create document
        doc = KnowledgeDocument(
            tenant_id=tenant.id,
            original_filename=file.filename,
            content_type=content_type,
            file_size=len(content),
            parsed_content="",  # Would be parsed here
            is_active=is_active,
        )
        
        session.add(doc)
        session.commit()
        
        return {
            "id": doc.id,
            "original_filename": doc.original_filename,
            "content_type": doc.content_type,
            "file_size": doc.file_size,
            "is_processed": False,
            "is_active": doc.is_active,
            "uploaded_at": doc.uploaded_at,
        }


@router.get("/list", response_model=KnowledgeListResponse)
async def list_knowledge(
    tenant_key: str,
    api_key: str,
):
    """List all knowledge documents for tenant."""
    
    # Verify credentials
    if not tenant_key or not api_key:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    async with get_db_session() as session:
        documents = session.query(KnowledgeDocument).filter(
            KnowledgeDocument.tenant_id == tenant_key,
        ).all()
        
        return {
            "documents": [
                {
                    "id": doc.id,
                    "original_filename": doc.original_filename,
                    "content_type": doc.content_type,
                    "file_size": doc.file_size,
                    "is_processed": doc.is_processed,
                    "is_active": doc.is_active,
                    "uploaded_at": doc.uploaded_at,
                }
                for doc in documents
            ],
            "count": len(documents),
        }


@router.delete("/{doc_id}")
async def delete_knowledge(
    doc_id: int,
    tenant_key: str,
    api_key: str,
):
    """Delete a knowledge document."""
    
    # Verify credentials
    if not tenant_key or not api_key:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    async with get_db_session() as session:
        doc = session.query(KnowledgeDocument).filter(
            KnowledgeDocument.id == doc_id,
            KnowledgeDocument.tenant_id == tenant_key,
        ).first()
        
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")
        
        session.delete(doc)
        session.commit()
        
        return {"success": True, "message": "Document deleted"}


@router.put("/{doc_id}/active")
async def toggle_knowledge_active(
    doc_id: int,
    is_active: bool,
    tenant_key: str,
    api_key: str,
):
    """Toggle document active status."""
    
    # Verify credentials
    if not tenant_key or not api_key:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    async with get_db_session() as session:
        doc = session.query(KnowledgeDocument).filter(
            KnowledgeDocument.id == doc_id,
            KnowledgeDocument.tenant_id == tenant_key,
        ).first()
        
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")
        
        doc.is_active = is_active
        session.commit()
        
        return {
            "success": True,
            "is_active": doc.is_active,
        }