"""
SC Chatbot E2E Tests

End-to-end tests for all project phases: POC, MVP, and Production.
"""

import pytest
from pages.admin import AdminPage
from pages.login import LoginPage
from pages.chat import ChatPage
from pages.knowledge import KnowledgePage


@pytest.fixture
def tenant1(page):
    """Create and login to tenant 1."""
    login_page = LoginPage(page)
    login_page.goto_and_login(
        tenant_key="test-tenant-1",
        email="admin@test.com",
        password="password123",
    )
    return login_page


@pytest.fixture
def tenant2(page):
    """Create and login to tenant 2."""
    login_page = LoginPage(page)
    login_page.goto_and_login(
        tenant_key="test-tenant-2",
        email="admin2@test.com",
        password="password123",
    )
    return login_page


class TestPOCPhase:
    """POC Phase Tests (Months 1-3)"""
    
    def test_poc_chatbot_response(self, tenant1):
        """Test that chatbot responds intelligently using RAG."""
        chat = ChatPage(tenant1)
        chat.new_conversation()
        chat.send_message("What is your product catalog?")
        chat.expect_response_to_contain("product", timeout=10000)
    
    def test_poc_tool_calling(self, tenant1):
        """Test that chatbot can call custom tools."""
        chat = ChatPage(tenant1)
        chat.new_conversation()
        chat.send_message("check_inventory")
        chat.expect_tool_call("check_inventory")
    
    def test_poc_knowledge_upload(self, tenant1):
        """Test uploading knowledge via basic UI."""
        knowledge = KnowledgePage(tenant1)
        knowledge.click_upload()
        # Would add actual file upload test
    
    def test_poc_conversation_memory(self, tenant1):
        """Test conversation memory (last 10 exchanges)."""
        chat = ChatPage(tenant1)
        chat.new_conversation()
        chat.send_message("Hello")
        chat.send_message("How are you?")
        chat.expect_last_message_to_contain("How are you?")


class TestMVPPhase:
    """MVP Phase Tests (Months 4-9)"""
    
    def test_mvp_multi_tenant_isolation(self, tenant1, tenant2):
        """Test multi-tenant data isolation."""
        chat1 = ChatPage(tenant1)
        chat1.new_conversation()
        chat1.send_message("test message")
        
        chat2 = ChatPage(tenant2)
        chat2.new_conversation()
        chat2.send_message("different message")
        
        # Verify tenants see different conversations
        chat1.get_conversations()
        chat2.get_conversations()
    
    def test_mvp_facebook_integration(self, tenant1):
        """Test Facebook Messenger integration."""
        chat = ChatPage(tenant1)
        chat.set_channel("facebook")
        chat.expect_facebook_page_configured()
    
    def test_mvp_full_analytics(self, tenant1):
        """Test advanced analytics dashboard."""
        admin = AdminPage(tenant1)
        admin.goto_analytics()
        admin.expect_analytics_displayed()
    
    def test_mvp_prometheus_grafana(self, tenant1):
        """Test Prometheus + Grafana monitoring."""
        # Would add monitoring tests
        pass


class TestProductionPhase:
    """Production Phase Tests (Months 10-21)"""
    
    def test_production_instagram(self, tenant1):
        """Test Instagram Direct integration."""
        chat = ChatPage(tenant1)
        chat.set_channel("instagram")
        chat.expect_instagram_business_account()
    
    def test_production_billing(self, tenant1):
        """Test billing & subscription management."""
        admin = AdminPage(tenant1)
        admin.goto_billing()
        admin.expect_subscription_plans()
    
    def test_production_high_availability(self, tenant1):
        """Test high availability & scaling."""
        admin = AdminPage(tenant1)
        admin.goto_settings()
        admin.click_enable_auto_scaling()
        admin.expect_auto_scaling_enabled()
    
    def test_production_qdrant(self, tenant1):
        """Test Qdrant vector database upgrade."""
        # Would add vector DB tests
        pass


class TestKnowledgeEndpoints:
    """Knowledge Management Tests"""
    
    def test_upload_pdf(self, tenant1):
        """Test uploading PDF documents."""
        knowledge = KnowledgePage(tenant1)
        knowledge.upload_file("sample.pdf")
        knowledge.expect_file_uploaded()
    
    def test_chunking_strategies(self, tenant1):
        """Test chunking strategies."""
        knowledge = KnowledgePage(tenant1)
        knowledge.click_configure_chunking()
        knowledge.expect_sentence_chunking()
        knowledge.expect_paragraph_chunking()
        knowledge.expect_semantic_chunking()
    
    def test_knowledge_refresh(self, tenant1):
        """Test knowledge refresh scheduler."""
        admin = AdminPage(tenant1)
        admin.click_configure_crawl_scheduler()
        admin.expect_daily_crawl()
        admin.expect_weekly_crawl()
    
    def test_vector_store_versioning(self, tenant1):
        """Test vector store versioning."""
        admin = AdminPage(tenant1)
        admin.click_create_version()
        admin.expect_version_created()
    
    def test_knowledge_metrics(self, tenant1):
        """Test knowledge search quality metrics."""
        admin = AdminPage(tenant1)
        admin.goto_knowledge_metrics()
        admin.expect_precision_metric()
        admin.expect_recall_metric()


class TestToolEndpoints:
    """Tool Management Tests"""
    
    def test_tool_definition(self, tenant1):
        """Test tool definition endpoints."""
        admin = AdminPage(tenant1)
        admin.goto_tools()
        admin.click_add_tool()
        admin.fill_tool_form("check_inventory", "Check product inventory")
        admin.submit_tool_form()
    
    def test_tool_execution(self, tenant1):
        """Test tool execution with parameters."""
        chat = ChatPage(tenant1)
        chat.send_message("check_inventory for SKU-123")
        chat.expect_tool_result()
    
    def test_tool_logging(self, tenant1):
        """Test tool call logging."""
        admin = AdminPage(tenant1)
        admin.goto_tool_logs()
        admin.expect_tool_calls_logged()
    
    def test_tool_error_handling(self, tenant1):
        """Test tool error handling."""
        chat = ChatPage(tenant1)
        chat.send_message("nonexistent_tool")
        chat.expect_error_message()


class TestAuthEndpoints:
    """Authentication Tests"""
    
    def test_tenant_registration(self, page):
        """Test tenant registration endpoint."""
        login = LoginPage(page)
        login.goto_register()
        login.fill_registration_form("test-key", "test@email.com", "password123", "Test Tenant")
        login.click_register()
        login.expect_login_successful()
    
    def test_login(self, tenant1):
        """Test login endpoint."""
        login = LoginPage(tenant1)
        login.goto_login()
        login.fill_form("test-tenant", "test@email.com", "password123")
        login.click_login()
        login.expect_dashboard_displayed()
    
    def test_token_refresh(self, tenant1):
        """Test token refresh mechanism."""
        # Would add token refresh tests
        pass
    
    def test_current_user(self, tenant1):
        """Test current user endpoint."""
        admin = AdminPage(tenant1)
        admin.goto_profile()
        admin.expect_user_info_displayed()


class TestAdminEndpoints:
    """Admin Dashboard Tests"""
    
    def test_analytics_endpoint(self, tenant1):
        """Test analytics dashboard."""
        admin = AdminPage(tenant1)
        admin.goto_analytics()
        admin.expect_total_messages_displayed()
        admin.expect_active_conversations_displayed()
        admin.expect_tool_calls_displayed()
    
    def test_users_list(self, tenant1):
        """Test user listing."""
        admin = AdminPage(tenant1)
        admin.goto_users()
        admin.expect_users_list_displayed()
    
    def test_documents_list(self, tenant1):
        """Test knowledge document listing."""
        admin = AdminPage(tenant1)
        admin.goto_knowledge()
        admin.expect_documents_list_displayed()
    
    def test_settings_get(self, tenant1):
        """Test getting tenant settings."""
        admin = AdminPage(tenant1)
        admin.goto_settings()
        admin.expect_settings_displayed()
    
    def test_settings_update(self, tenant1):
        """Test updating tenant settings."""
        admin = AdminPage(tenant1)
        admin.goto_settings()
        admin.fill_model_name("gpt-4o-mini")
        admin.click_save_settings()
        admin.expect_settings_saved()


class TestWebSocketEndpoints:
    """WebSocket Tests"""
    
    def test_websocket_chat(self, tenant1):
        """Test WebSocket chat streaming."""
        chat = ChatPage(tenant1)
        chat.connect_websocket()
        chat.send_message("Hello")
        chat.expect_streaming_response()
    
    def test_websocket_ping_pong(self, tenant1):
        """Test WebSocket ping/pong."""
        chat = ChatPage(tenant1)
        chat.send_ping()
        chat.expect_pong_response()