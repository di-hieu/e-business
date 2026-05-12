"""
Admin Dashboard E2E Tests

Tests for admin dashboard functionality using Playwright.
"""

import pytest
from playwright.sync_api import Page, expect


# ========================================================================
# ADMIN DASHBOARD E2E TEST CASES
# ========================================================================

class TestAdminDashboardLogin:
    """Test admin dashboard login functionality."""

    @pytest.mark.e2e
    @pytest.mark.admin
    def test_admin_login_page_loads(self, page: Page):
        """Test that login page loads successfully."""
        # Navigate to login page
        page.goto("/admin/login")

        # Verify login form exists
        expect(page.locator("form[name='login-form']")).to_be_visible()
        expect(page.locator("input[name='email']")).to_be_enabled()
        expect(page.locator("input[name='password']")).to_be_enabled()

    @pytest.mark.e2e
    @pytest.mark.admin
    def test_admin_login_success(self, page: Page):
        """Test successful login to admin dashboard."""
        # Navigate to login page
        page.goto("/admin/login")

        # Fill in login credentials
        page.fill("input[name='email']", "admin@example.com")
        page.fill("input[name='password']", "admin123")

        # Click login button
        page.click("button[type='submit']")

        # Verify redirect to dashboard
        expect(page.url).to_contain("/admin/dashboard")

    @pytest.mark.e2e
    @pytest.mark.admin
    def test_admin_login_failure(self, page: Page):
        """Test login failure with invalid credentials."""
        # Navigate to login page
        page.goto("/admin/login")

        # Fill in invalid credentials
        page.fill("input[name='email']", "wrong@example.com")
        page.fill("input[name='password']", "wrongpassword")

        # Click login button
        page.click("button[type='submit']")

        # Verify error message
        expect(page.locator(".error-message")).to_contain_text("Invalid credentials")

    @pytest.mark.e2e
    @pytest.mark.admin
    def test_admin_logout(self, page: Page):
        """Test admin logout functionality."""
        # Navigate to dashboard
        page.goto("/admin/dashboard")

        # Click logout button
        page.click("button:has-text('Logout')")

        # Verify redirect to login
        expect(page.url).to_contain("/admin/login")


# ========================================================================
# KNOWLEDGE BASE MANAGEMENT TESTS
# ========================================================================

class TestKnowledgeBaseManagement:
    """Test knowledge base management functionality."""

    @pytest.mark.e2e
    @pytest.mark.admin
    def test_knowledge_base_list(self, page: Page):
        """Test knowledge base list view."""
        # Navigate to knowledge base management
        page.goto("/admin/knowledge")

        # Verify knowledge base list is visible
        expect(page.locator(".kb-list")).to_be_visible()

    @pytest.mark.e2e
    @pytest.mark.admin
    def test_upload_knowledge_file(self, page: Page):
        """Test uploading knowledge files."""
        # Navigate to knowledge management
        page.goto("/admin/knowledge/upload")

        # Select file to upload
        file_chooser = page.wait_for_selector("input[type='file']")
        file_chooser.set_input_files("test/fixtures/data/sample_documents.json")

        # Click upload button
        page.click("button:has-text('Upload')")

        # Verify upload success message
        expect(page.locator(".upload-success")).to_be_visible()

    @pytest.mark.e2e
    @pytest.mark.admin
    def test_knowledge_search(self, page: Page):
        """Test knowledge base search functionality."""
        # Navigate to knowledge management
        page.goto("/admin/knowledge")

        # Enter search query
        page.fill("input[name='search']", "return policy")

        # Press enter to search
        page.press("input[name='search']", "Enter")

        # Verify search results
        expect(page.locator(".search-results")).to_be_visible()

    @pytest.mark.e2e
    @pytest.mark.admin
    def test_knowledge_delete(self, page: Page):
        """Test deleting knowledge documents."""
        # Navigate to knowledge management
        page.goto("/admin/knowledge")

        # Click delete button on a document
        page.click("button:has-text('Delete')")

        # Verify confirmation dialog
        expect(page.locator(".confirm-dialog")).to_be_visible()

        # Confirm deletion
        page.click("button:has-text('Confirm')")

        # Verify document is removed
        expect(page.locator(".kb-list")).to_not_contain("Deleted Document")


# ========================================================================
# TOOL MANAGEMENT TESTS
# ========================================================================

class TestToolManagement:
    """Test tool management functionality."""

    @pytest.mark.e2e
    @pytest.mark.admin
    def test_tool_list(self, page: Page):
        """Test tool list view."""
        # Navigate to tools management
        page.goto("/admin/tools")

        # Verify tools list is visible
        expect(page.locator(".tool-list")).to_be_visible()

    @pytest.mark.e2e
    @pytest.mark.admin
    def test_add_new_tool(self, page: Page):
        """Test adding a new tool."""
        # Navigate to tools management
        page.goto("/admin/tools")

        # Click add tool button
        page.click("button:has-text('Add Tool')")

        # Fill in tool details
        page.fill("input[name='tool_name']", "check_order_status")
        page.fill("textarea[name='description']", "Check order status")
        page.fill("input[name='endpoint']", "/api/orders/status")

        # Click save button
        page.click("button:has-text('Save')")

        # Verify success message
        expect(page.locator(".success-message")).to_contain_text("Tool created")

    @pytest.mark.e2e
    @pytest.mark.admin
    def test_tool_parameter_schema(self, page: Page):
        """Test tool parameter schema editor."""
        # Navigate to tools management
        page.goto("/admin/tools")

        # Click on a tool to edit
        page.click(".tool-card")

        # Verify schema editor is visible
        expect(page.locator("textarea[name='schema']")).to_be_visible()

    @pytest.mark.e2e
    @pytest.mark.admin
    def test_tool_test_button(self, page: Page):
        """Test tool testing functionality."""
        # Navigate to tools management
        page.goto("/admin/tools")

        # Click test button on a tool
        page.click("button:has-text('Test')")

        # Verify test response is displayed
        expect(page.locator(".test-response")).to_be_visible()


# ========================================================================
# CONVERSATION MANAGEMENT TESTS
# ========================================================================

class TestConversationManagement:
    """Test conversation management functionality."""

    @pytest.mark.e2e
    @pytest.mark.admin
    def test_conversation_list(self, page: Page):
        """Test conversation list view."""
        # Navigate to conversations
        page.goto("/admin/conversations")

        # Verify conversations list is visible
        expect(page.locator(".conversation-list")).to_be_visible()

    @pytest.mark.e2e
    @pytest.mark.admin
    def test_view_conversation_details(self, page: Page):
        """Test viewing conversation details."""
        # Navigate to conversations
        page.goto("/admin/conversations")

        # Click on a conversation
        page.click(".conversation-item")

        # Verify conversation details are visible
        expect(page.locator(".conversation-detail")).to_be_visible()

    @pytest.mark.e2e
    @pytest.mark.admin
    def test_export_conversations(self, page: Page):
        """Test exporting conversations to CSV."""
        # Navigate to conversations
        page.goto("/admin/conversations")

        # Click export button
        page.click("button:has-text('Export')")

        # Verify download starts
        expect(page.locator(".download-indicator")).to_be_visible()

    @pytest.mark.e2e
    @pytest.mark.admin
    def test_archive_conversation(self, page: Page):
        """Test archiving a conversation."""
        # Navigate to conversations
        page.goto("/admin/conversations")

        # Click archive button
        page.click("button:has-text('Archive')")

        # Verify conversation is moved to archive
        expect(page.locator(".archive-indicator")).to_be_visible()


# ========================================================================
# ANALYTICS DASHBOARD TESTS
# ========================================================================

class TestAnalyticsDashboard:
    """Test analytics dashboard functionality."""

    @pytest.mark.e2e
    @pytest.mark.admin
    def test_analytics_page_loads(self, page: Page):
        """Test analytics page loads with data."""
        # Navigate to analytics
        page.goto("/admin/analytics")

        # Verify charts are visible
        expect(page.locator(".chart")).to_be_visible()

    @pytest.mark.e2e
    @pytest.mark.admin
    def test_analytics_filters(self, page: Page):
        """Test analytics filtering."""
        # Navigate to analytics
        page.goto("/admin/analytics")

        # Select date range filter
        page.select_option("select[name='date_range']", "last_7_days")

        # Verify filtered data is displayed
        expect(page.locator(".chart")).to_contain_text("Last 7 Days")

    @pytest.mark.e2e
    @pytest.mark.admin
    def test_analytics_tenant_filter(self, page: Page):
        """Test filtering analytics by tenant."""
        # Navigate to analytics
        page.goto("/admin/analytics")

        # Select tenant filter
        page.select_option("select[name='tenant']")

        # Verify filtered data
        expect(page.locator(".tenant-filter")).to_be_visible()

    @pytest.mark.e2e
    @pytest.mark.admin
    def test_analytics_response_time_chart(self, page: Page):
        """Test response time chart visualization."""
        # Navigate to analytics
        page.goto("/admin/analytics")

        # Verify response time chart is visible
        expect(page.locator(".response-time-chart")).to_be_visible()


# ========================================================================
# CHANNEL INTEGRATION TESTS
# ========================================================================

class TestChannelIntegration:
    """Test channel integration management."""

    @pytest.mark.e2e
    @pytest.mark.admin
    def test_channel_list(self, page: Page):
        """Test channel list view."""
        # Navigate to channels
        page.goto("/admin/channels")

        # Verify channels are listed
        expect(page.locator(".channel-list")).to_be_visible()

    @pytest.mark.e2e
    @pytest.mark.admin
    def test_zalo_channel_setup(self, page: Page):
        """Test Zalo channel setup."""
        # Navigate to Zalo channel settings
        page.goto("/admin/channels/zalo")

        # Fill in Zalo credentials
        page.fill("input[name='client_id']", "test_client_id")
        page.fill("input[name='client_secret']", "test_secret")
        page.fill("input[name='webhook_url']", "http://localhost:8000/webhooks/zalo")

        # Click save
        page.click("button:has-text('Save')")

        # Verify success
        expect(page.locator(".success-message")).to_contain_text("Channel configured")

    @pytest.mark.e2e
    @pytest.mark.admin
    def test_facebook_channel_setup(self, page: Page):
        """Test Facebook channel setup."""
        # Navigate to Facebook channel settings
        page.goto("/admin/channels/facebook")

        # Fill in Facebook credentials
        page.fill("input[name='app_id']", "test_app_id")
        page.fill("input[name='app_secret']", "test_secret")
        page.fill("input[name='verify_token']", "test_token")

        # Click save
        page.click("button:has-text('Save')")

        # Verify success
        expect(page.locator(".success-message")).to_be_visible()


# ========================================================================
# USER MANAGEMENT TESTS
# ========================================================================

class TestUserManagement:
    """Test user management functionality."""

    @pytest.mark.e2e
    @pytest.mark.admin
    def test_user_list(self, page: Page):
        """Test user list view."""
        # Navigate to users
        page.goto("/admin/users")

        # Verify users list is visible
        expect(page.locator(".user-list")).to_be_visible()

    @pytest.mark.e2e
    @pytest.mark.admin
    def test_add_user(self, page: Page):
        """Test adding a new user."""
        # Navigate to users
        page.goto("/admin/users")

        # Click add user button
        page.click("button:has-text('Add User')")

        # Fill in user details
        page.fill("input[name='email']", "newuser@example.com")
        page.fill("input[name='name']", "New User")
        page.select_option("select[name='role']", "agent")

        # Click save
        page.click("button:has-text('Save')")

        # Verify success
        expect(page.locator(".success-message")).to_contain_text("User created")

    @pytest.mark.e2e
    @pytest.mark.admin
    def test_edit_user_role(self, page: Page):
        """Test editing user role."""
        # Navigate to users
        page.goto("/admin/users")

        # Click on user to edit
        page.click(".user-row")

        # Change role
        page.select_option("select[name='role']", "admin")

        # Save changes
        page.click("button:has-text('Save')")

        # Verify role changed
        expect(page.locator(".user-role")).to_contain_text("admin")


# ========================================================================
# SETTINGS MANAGEMENT TESTS
# ========================================================================

class TestSettingsManagement:
    """Test settings management functionality."""

    @pytest.mark.e2e
    @pytest.mark.admin
    def test_settings_page_loads(self, page: Page):
        """Test settings page loads."""
        # Navigate to settings
        page.goto("/admin/settings")

        # Verify settings form is visible
        expect(page.locator(".settings-form")).to_be_visible()

    @pytest.mark.e2e
    @pytest.mark.admin
    def test_llm_settings(self, page: Page):
        """Test LLM settings configuration."""
        # Navigate to settings
        page.goto("/admin/settings")

        # Select LLM model
        page.select_option("select[name='llm_model']", "gpt-4o-mini")
        page.fill("input[name='api_key']", "test_api_key")

        # Click save
        page.click("button:has-text('Save')")

        # Verify success
        expect(page.locator(".success-message")).to_be_visible()

    @pytest.mark.e2e
    @pytest.mark.admin
    def test_response_style_settings(self, page: Page):
        """Test response style settings."""
        # Navigate to settings
        page.goto("/admin/settings")

        # Select response style
        page.select_option("select[name='response_style']", "friendly")

        # Click save
        page.click("button:has-text('Save')")

        # Verify success
        expect(page.locator(".success-message")).to_be_visible()


if __name__ == "__main__":
    pytest.main(["-v", __file__])