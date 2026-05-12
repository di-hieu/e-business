"""
E2E Test Fixtures

Helper functions for creating test data in E2E tests.
"""

import uuid
from typing import Dict, List, Any, Optional
from models import Tenant, Conversation, KnowledgeBase, Tool, User


def create_test_tenant(
    name: str = "Test Tenant",
    settings: Optional[Dict[str, Any]] = None
) -> Tenant:
    """Create a test tenant for E2E testing."""
    
    if settings is None:
        settings = {
            "llm_model": "gpt-4o-mini",
            "response_style": "friendly",
            "language": "en",
            "timezone": "Asia/Ho_Chi_Minh"
        }
    
    return Tenant(
        id=1,
        name=name,
        api_key=f"test_{uuid.uuid4().hex[:16]}",
        settings=settings
    )


def create_test_user(
    tenant_id: int,
    email: str = "test@example.com",
    name: str = "Test User",
    role: str = "admin"
) -> User:
    """Create a test user for E2E testing."""
    
    return User(
        id=1,
        tenant_id=tenant_id,
        email=email,
        name=name,
        password_hash="hashed_password_for_testing",
        role=role
    )


def create_test_conversation(
    tenant_id: int,
    channel: str = "zalo",
    status: str = "active"
) -> Conversation:
    """Create a test conversation for E2E testing."""
    
    return Conversation(
        id=1,
        tenant_id=tenant_id,
        user_id=1,
        channel=channel,
        messages=[],
        status=status
    )


def create_test_knowledge_base(
    tenant_id: int,
    name: str = "Test Knowledge Base",
    documents: Optional[List[Dict]] = None
) -> KnowledgeBase:
    """Create a test knowledge base for E2E testing."""
    
    sample_documents = [
        {
            "id": "kb_doc1",
            "title": "Return Policy",
            "content": "We offer a 30-day return policy for all products.",
            "category": "faq",
            "source": "upload"
        },
        {
            "id": "kb_doc2",
            "title": "Shipping Policy",
            "content": "Standard shipping takes 3-5 business days.",
            "category": "faq",
            "source": "upload"
        }
    ]
    
    return KnowledgeBase(
        id=1,
        tenant_id=tenant_id,
        name=name,
        documents=documents or sample_documents
    )


def create_test_tool(
    tenant_id: int,
    name: str = "check_inventory",
    parameters: Optional[Dict] = None
) -> Tool:
    """Create a test tool for E2E testing."""
    
    sample_parameters = {
        "type": "object",
        "properties": {
            "product_id": {"type": "string"},
            "warehouse": {"type": "string"}
        },
        "required": ["product_id"]
    }
    
    return Tool(
        id=1,
        tenant_id=tenant_id,
        name=name,
        description="Check product inventory",
        parameters=parameters or sample_parameters,
        endpoint="/api/inventory/check",
        method="POST"
    )


def create_sample_messages(
    conversation_id: int,
    role: str = "user",
    content: str = "Hello, how can I help?",
    metadata: Optional[Dict] = None
) -> Dict:
    """Create a sample message for testing."""
    
    return {
        "id": str(uuid.uuid4()),
        "conversation_id": conversation_id,
        "role": role,
        "content": content,
        "metadata": metadata or {},
        "timestamp": None  # Would be set by database
    }


def create_webhook_payload(channel: str, payload: Dict) -> Dict:
    """Create a webhook payload for testing."""
    
    return {
        "event_type": "message",
        "channel": channel,
        "data": payload,
        "timestamp": None
    }


def create_expected_responses() -> Dict[str, str]:
    """Create expected LLM responses for testing."""
    
    return {
        "greeting": "Hello! I'm here to help with your orders and questions.",
        "farewell": "Thank you for shopping with us! Have a great day!",
        "return_policy": "We offer a 30-day return policy. Items must be in their original condition with tags attached.",
        "shipping_info": "Standard shipping takes 3-5 business days. Express shipping is available for an additional fee.",
        "order_tracking": "To track your order, please provide your order number.",
        "unknown_question": "I'm not sure about that. Let me check with a human agent.",
        "tool_error": "I'm having trouble accessing that information. Please try again later."
    }