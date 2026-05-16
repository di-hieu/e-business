"""
Shared fixtures for E2E testing.
"""

import pytest
import sys
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import uuid
import shutil

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.backend import models
from src.backend.config import settings


@pytest.fixture(scope="session")
def test_db():
    """Create a test database for E2E testing."""
    test_db_path = settings.test_db_path
    
    # Create test database
    models.Base.metadata.create_all(test_db)
    
    yield test_db
    
    # Cleanup after tests
    if settings.cleanup_on_finish:
        models.Base.metadata.drop_all(test_db)


@pytest.fixture
def sample_tenant(test_db):
    """Create a sample tenant for testing."""
    from models import Tenant
    return Tenant(
        id=1,
        name="Test Tenant",
        api_key=f"test_{uuid.uuid4().hex[:16]}",
        settings={
            "llm_model": "gpt-4o-mini",
            "response_style": "friendly",
            "language": "en"
        }
    )


@pytest.fixture
def sample_user(sample_tenant):
    """Create a sample user for testing."""
    from models import User
    return User(
        id=1,
        tenant_id=sample_tenant.id,
        email="test@example.com",
        name="Test User",
        password_hash="hashed_password_for_testing",
        role="admin"
    )


@pytest.fixture
def sample_conversation(sample_tenant, sample_user):
    """Create a sample conversation for testing."""
    from models import Conversation
    return Conversation(
        id=1,
        tenant_id=sample_tenant.id,
        user_id=sample_user.id,
        channel="zalo",
        messages=[],
        status="active"
    )


@pytest.fixture
def sample_knowledge_base(sample_tenant):
    """Create a sample knowledge base for testing."""
    from models import KnowledgeBase
    
    return KnowledgeBase(
        id=1,
        tenant_id=sample_tenant.id,
        name="Test Knowledge Base",
        documents=[
            {
                "id": "kb_doc1",
                "title": "Return Policy",
                "content": "We offer a 30-day return policy for all products.",
                "category": "faq",
                "source": "upload"
            }
        ]
    )


@pytest.fixture
def mock_llm():
    """Mock LLM responses for testing."""
    return {
        "greeting": "Hello! I'm here to help with your orders and questions.",
        "farewell": "Thank you for shopping with us! Have a great day!",
        "return_policy": "We offer a 30-day return policy. Items must be in their original condition with tags attached.",
        "shipping_info": "Standard shipping takes 3-5 business days.",
        "unknown": "I'm not sure about that. Let me check with a human agent."
    }


@pytest.fixture
def mock_tools():
    """Mock tool responses for testing."""
    return {
        "check_inventory": {
            "result": {"status": "success", "count": 100},
            "error": "Inventory not found"
        },
        "track_order": {
            "result": {"status": "success", "tracking_number": "TEST123", "estimated_delivery": "2026-05-15"},
            "error": "Order not found"
        },
        "book_tour": {
            "result": {"status": "success", "booking_id": "BK12345", "message": "Tour booked successfully"},
            "error": "Unable to book tour"
        }
    }


@pytest.fixture
def mock_vector_store():
    """Mock vector store for testing."""
    return {
        "similarity_search": lambda query, k: [
            {"content": "Sample vector 1 content", "score": 0.95},
            {"content": "Sample vector 2 content", "score": 0.87}
        ],
        "add": lambda doc: True
    }


@pytest.fixture
def browser_context():
    """Browser context for Playwright E2E tests."""
    # This fixture would be used with Playwright
    # Setup would go here
    return {
        "browser_type": "chromium",
        "headless": True,
        "viewport": {"width": 1920, "height": 1080}
    }


@pytest.fixture
def webhook_zalo():
    """Mock Zalo webhook payload for testing."""
    return {
        "event_type": "message",
        "data": {
            "from": "123456789",
            "to": "987654321",
            "content_type": "text",
            "content": "Hello, I want to return my order",
            "timestamp": datetime.utcnow().isoformat()
        }
    }


@pytest.fixture
def webhook_facebook():
    """Mock Facebook webhook payload for testing."""
    return {
        "message": {
            "from": {"id": "user123"},
            "message": "Hi there!",
            "timestamp": datetime.utcnow().isoformat()
        }
    }


@pytest.fixture
def webhook_instagram():
    """Mock Instagram webhook payload for testing."""
    return {
        "entry": [{
            "id": "ig_page_id",
            "time": datetime.utcnow().isoformat(),
            "messaging": [{
                "sender": {"id": "user123"},
                "message": {"text": "Hello"}
            }]
        }]
    }


@pytest.fixture
def expected_responses():
    """Expected LLM responses for testing."""
    return {
        "greeting": "Hello! I'm here to help with your orders and questions.",
        "farewell": "Thank you for shopping with us! Have a great day!",
        "return_policy": "We offer a 30-day return policy for all products.",
        "shipping_info": "Standard shipping takes 3-5 business days.",
        "order_tracking": "To track your order, please provide your order number.",
        "unknown_question": "I'm not sure about that. Let me check with a human agent."
    }


@pytest.fixture
def test_config():
    """Test configuration."""
    from src.backend.e2e.config import E2EConfig
    config = E2EConfig()
    config.test_mode = True
    return config


@pytest.fixture(scope="function")
def temp_test_dir():
    """Create a temporary directory for test fixtures."""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    # Cleanup
    if True:  # settings.cleanup_on_finish:
        shutil.rmtree(temp_dir, ignore_errors=True)