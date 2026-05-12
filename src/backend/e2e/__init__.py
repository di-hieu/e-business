"""
E2E Testing Support Module

End-to-end testing utilities and configuration for SC Chatbot platform.
Provides test clients, mock services, and testing helpers for comprehensive E2E test coverage.
"""

from .config import E2EConfig
from .fixtures import (
    create_test_tenant,
    create_test_conversation,
    create_test_knowledge_base,
    create_test_tool,
)
from .websockets import E2EWebSocketHandler
from .messaging import E2EMessageProcessor
from .test_client import E2ETestClient

__all__ = [
    "E2EConfig",
    "E2ETestClient",
    "E2EWebSocketHandler",
    "E2EMessageProcessor",
    "create_test_tenant",
    "create_test_conversation",
    "create_test_knowledge_base",
    "create_test_tool",
]