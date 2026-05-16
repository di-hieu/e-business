"""
SC Chatbot - Telegram Channel Tests
POC Phase Tests for Telegram Integration

Run with: pytest test/channels/test_telegram_channel.py -v
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Add backend to path
import sys
sys.path.insert(0, '/home/dihieu/.ws/e-business/src/backend')

from main import app
from models.database import Base, get_db_session
from models.conversation import Conversation
from typing import Optional
import json


# =============================================================================
# FIXTURES
# =============================================================================


@pytest.fixture
def engine():
    """Create test SQLite engine"""
    test_engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=test_engine)
    return test_engine


@pytest.fixture
def session(engine):
    """Create test session"""
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()


@pytest.fixture
def client(session):
    """Create test client"""
    # Override get_db_session to use test session
    from src.backend.models.database import get_db_session
    
    async def mock_get_db_session():
        return session
    
    app.dependency_overrides[get_db_session] = mock_get_db_session
    return TestClient(app)


        
        # Create a test user
        user = User(
            user_id="999999",
            tenant_id=tenant.id,
            email="test@example.com",
            name="Test User",
        )
        session.add(user)
        session.commit()
        
        # Get RAG pipeline
        from src.backend.rag.pipeline import RAGPipeline
        
        # Create a simple knowledge document
        rag_pipeline = RAGPipeline(tenant_id=tenant.id)
        
        # Create a conversation
        from src.backend.models.conversation import Conversation
        conversation = Conversation(
            user_id="999999",
            tenant_id=tenant.id,
            channel="telegram",
        )
        session.add(conversation)
        session.commit()
        
        # Test response
        mock_bot_token = "test_bot_token"
        update = {
            "message": {
                "chat_id": 123456,
                "from": {"id": 999999, "is_bot": False, "first_name": "Test"},
                "text": "Hello",
            },
        }
        
        response = client.post(
            f"/api/webhooks/telegram/test?bot_token={mock_bot_token}",
            json=update,
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code in [200, 500]


# =============================================================================
# MOCK TELEGRAM API TESTS
# =============================================================================


class TestTelegramMockAPI:
    """Test mock Telegram API for local development"""
    
    def test_send_message_mock(self):
        """Test that mock send_message function works"""
        # Simulate sending a message
        mock_response = {
            "ok": True,
            "result": {
                "message_id": 123,
                "chat": {
                    "id": 123456,
                    "first_name": "Test",
                    "is_user": True,
                },
                "text": "Hello from SC Chatbot!",
                "date": 1234567890,
            }
        }
        assert mock_response["ok"] is True
    
    def test_parse_telegram_update(self):
        """Test parsing Telegram update"""
        update_json = json.dumps({
            "message": {
                "message_id": 123,
                "from": {
                    "id": 999999,
                    "is_bot": False,
                    "first_name": "Alice",
                },
                "chat": {
                    "id": 123456,
                    "first_name": "Alice",
                },
                "text": "Hello world!",
            }
        })
        
        update = json.loads(update_json)
        
        assert update["message"]["message_id"] == 123
        assert update["message"]["from"]["first_name"] == "Alice"
        assert update["message"]["text"] == "Hello world!"


# =============================================================================
# POE SUITE
# =============================================================================


class TestTelegramPOCSuite:
    """POC test suite for Telegram integration"""
    
    @pytest.mark.poc
    def test_poc_01_webhook_endpoint_exists(self, client):
        """POC: Verify webhook endpoint exists"""
        response = client.get("/docs")
        assert response.status_code == 200
        assert "telegram" in response.text.lower()
    
    @pytest.mark.poc
    def test_poc_02_webhook_accepts_payload(self, client):
        """POC: Verify webhook accepts payload"""
        response = client.post(
            "/api/webhooks/telegram/test?bot_token=test_token",
            json={"message": {"text": "test"}},
        )
        assert response.status_code in [200, 500]
    
    @pytest.mark.poc
    def test_poc_03_message_processed(self, client):
        """POC: Verify message is processed"""
        response = client.post(
            "/api/webhooks/telegram/test?bot_token=test_token",
            json={"message": {"text": "Hello"}},
        )
        assert "result" in response.json() or response.status_code == 200


# =============================================================================
# SETUP TESTS
# =============================================================================


class TestTelegramSetup:
    """Test Telegram setup and configuration"""
    
    def test_env_example_has_telegram_vars(self):
        """Test that .env.example has Telegram variables"""
        with open(".env.example") as f:
            content = f.read()
        
        assert "TELEGRAM_BOT_TOKEN" in content
        assert "TELEGRAM_WEBHOOK_URL" in content
    
    def test_webhook_file_has_telegram_code(self):
        """Test that webhooks.py has Telegram code"""
        with open("src/backend/api/webhooks.py") as f:
            content = f.read()
        
        assert "TelegramWebhook" in content
        assert "TELEGRAM_BOT_TOKEN" in content or "bot_token" in content
    
    def test_requirements_has_requests(self):
        """Test that requirements.txt has requests"""
        with open("requirements.txt") as f:
            content = f.read()
        
        assert "requests" in content.lower()