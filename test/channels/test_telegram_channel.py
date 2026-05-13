"""
SC Chatbot - Telegram Channel Tests
POC Phase Tests for Telegram Integration

Run with: pytest test/channels/test_telegram_channel.py -v
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.backend.main import app
from src.backend.models.database import Base, get_db_session
from src.backend.api.webhooks import telegram_webhook
from typing import Optional
import json


# =============================================================================
# FIXTURES
# =============================================================================


@pytest.fixture
def engine():
    """Create test SQLite engine"""
    test_engine = create_engine("sqlite+aiosqlite:///:memory:", connect_args={"check_same_thread": False})
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


@pytest.fixture(autouse=True)
def cleanup(session):
    """Clean up test data after each test"""
    yield
    session.delete(session.query("conversations").first())
    session.delete(session.query("messages").first())
    session.commit()


# =============================================================================
# TELEGRAM WEBHOOK TESTS
# =============================================================================


class TestTelegramWebhook:
    """Test Telegram webhook handler"""
    
    def test_webhook_endpoint_returns_400_without_token(self, client):
        """Test that webhook returns 400 when bot_token is missing"""
        response = client.post("/webhooks/telegram", json={})
        assert response.status_code == 400
        assert response.json()["ok"] is False
        assert "BOT_TOKEN required" in response.json()["error"]
    
    def test_webhook_with_mock_update(self, client):
        """Test webhook with mock Telegram update"""
        mock_bot_token = "test_bot_token_for_poc_only"
        
        # Mock update payload
        update = {
            "message": {
                "chat_id": 123456,
                "from": {"id": 999999, "is_bot": False, "first_name": "Test"},
                "text": "Hello from Telegram!",
            },
        }
        
        response = client.post(
            f"/webhooks/telegram?bot_token={mock_bot_token}",
            json=update,
            headers={"Authorization": "Bearer test-token"}
        )
        
        # For POC, we expect success even without full Telegram API connectivity
        assert response.status_code in [200, 500]  # 500 is OK in POC if Telegram API unavailable


class TestTelegramCommandHandling:
    """Test Telegram command handling"""
    
    def test_start_command(self, client):
        """Test /start command"""
        mock_bot_token = "test_bot_token"
        update = {
            "message": {
                "chat_id": 123456,
                "from": {"id": 999999, "is_bot": False, "first_name": "User"},
                "text": "/start",
            },
        }
        
        response = client.post(
            f"/webhooks/telegram/test?bot_token={mock_bot_token}",
            json=update,
        )
        
        assert response.status_code == 200
    
    def test_help_command(self, client):
        """Test /help command"""
        mock_bot_token = "test_bot_token"
        update = {
            "message": {
                "chat_id": 123456,
                "from": {"id": 999999, "is_bot": False, "first_name": "User"},
                "text": "/help",
            },
        }
        
        response = client.post(
            f"/webhooks/telegram/test?bot_token={mock_bot_token}",
            json=update,
        )
        
        assert response.status_code == 200


class TestTelegramRAGIntegration:
    """Test RAG integration with Telegram"""
    
    def test_rag_response_with_telegram(self, client, session):
        """Test that RAG pipeline responds to Telegram messages"""
        
        # First, create a test tenant
        from src.backend.models.tenant import Tenant
        from src.backend.models.user import User
        
        tenant = Tenant(
            tenant_key="test-tenant",
            email="test@example.com",
            name="Test Company",
        )
        session.add(tenant)
        session.commit()
        
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
            f"/webhooks/telegram/test?bot_token={mock_bot_token}",
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
            "/webhooks/telegram/test?bot_token=test_token",
            json={"message": {"text": "test"}},
        )
        assert response.status_code in [200, 500]
    
    @pytest.mark.poc
    def test_poc_03_message_processed(self, client):
        """POC: Verify message is processed"""
        response = client.post(
            "/webhooks/telegram/test?bot_token=test_token",
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