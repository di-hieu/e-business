"""
Locust Load Testing Configuration

Load testing scripts for the SC Chatbot platform.
"""

from locust import HttpUser, task, between, events
from datetime import datetime


class ChatbotUser(HttpUser):
    """Simulates a chatbot user interaction."""
    
    wait_time = between(1, 3)
    
    def on_start(self):
        """Called when a user starts."""
        self.login()
    
    @task(3)
    def login(self):
        """Simulate login."""
        with self.client.post("/api/auth/login", catch_response=True) as response:
            if response.status_code == 200:
                self.user_data = response.json()
                response.success()
            else:
                response.failure("Login failed")
    
    @task(5)
    def send_message(self):
        """Simulate sending a chat message."""
        # Would use WebSocket for real, but using HTTP for load testing
        messages = [
            "Hello, can you help me?",
            "What's your return policy?",
            "I want to track my order #12345",
            "Can I return this product?",
            "Thank you for your help!",
        ]
        
        with self.client.post("/api/chat/message", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure("Message send failed")
    
    @task(2)
    def view_conversations(self):
        """Simulate viewing conversation history."""
        with self.client.get("/api/conversations", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure("Failed to fetch conversations")
    
    @task(1)
    def upload_knowledge(self):
        """Simulate knowledge upload (less frequent)."""
        with self.client.post(
            "/api/knowledge/upload",
            files={"file": ("sample.pdf", b"binary content")},
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure("Knowledge upload failed")


class AdminUser(HttpUser):
    """Simulates an admin user."""
    
    wait_time = between(2, 5)
    
    def on_start(self):
        self.login_admin()
    
    @task(3)
    def view_dashboard(self):
        """Simulate viewing admin dashboard."""
        with self.client.get("/api/admin/dashboard", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure("Dashboard access failed")
    
    @task(2)
    def manage_tenant(self):
        """Simulate tenant management."""
        with self.client.post("/api/admin/tenants", catch_response=True) as response:
            if response.status_code == 201:
                response.success()
            else:
                response.failure("Tenant creation failed")


class BotHealthCheck(HttpUser):
    """Health check monitoring."""
    
    wait_time = between(10, 30)
    
    @task(1)
    def health_check(self):
        """Simulate health check requests."""
        with self.client.get("/health", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure("Health check failed")


# Events for reporting
@events.test_start.add_listener
def on_test_start(environment, *args, **kwargs):
    """Called when test starts."""
    print(f"\n=== Load Test Starting at {datetime.utcnow().isoformat()} ===")


@events.test_stop.add_listener
def on_test_stop(environment, *args, **kwargs):
    """Called when test stops."""
    print(f"\n=== Load Test Completed at {datetime.utcnow().isoformat()} ===")