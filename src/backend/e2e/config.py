"""
E2E Test Configuration

Configuration settings for end-to-end testing.
"""

import os
from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class E2EConfig:
    """End-to-end testing configuration."""
    
    # Test environment
    test_mode: bool = False
    debug_mode: bool = False
    
    # Database settings
    test_db_path: str = "test_db.sqlite"
    test_db_url: str = "sqlite:///test_db.sqlite"
    test_db_timeout: float = 30.0  # seconds
    
    # WebSocket test settings
    ws_test_timeout: float = 30.0
    ws_test_reconnect_delay: float = 2.0
    ws_test_max_reconnects: int = 5
    
    # Message test settings
    message_test_batch_size: int = 100
    message_test_chunk_size: int = 256
    
    # Test rate limiting
    test_rate_limit_per_minute: int = 1000
    test_concurrent_users: int = 100
    
    # Test cleanup settings
    cleanup_on_finish: bool = True
    cleanup_timeout: float = 10.0
    
    # Mock settings
    mock_llm_enabled: bool = True
    mock_vector_store_enabled: bool = True
    mock_webhook_enabled: bool = False
    
    # Test data settings
    use_mock_data: bool = True
    data_seed_limit: int = 1000
    
    @classmethod
    def from_env(cls) -> "E2EConfig":
        """Create config from environment variables."""
        config = cls()
        
        # Override from environment
        if os.environ.get("E2E_TEST_MODE", "").lower() in ("1", "true", "yes"):
            config.test_mode = True
        
        if os.environ.get("E2E_DEBUG_MODE", "").lower() in ("1", "true", "yes"):
            config.debug_mode = True
        
        if os.environ.get("E2E_MOCK_LLM", "").lower() in ("1", "true", "yes"):
            config.mock_llm_enabled = True
        
        if os.environ.get("E2E_USE_MOCK_DATA", "").lower() in ("1", "true", "yes"):
            config.use_mock_data = True
        
        if os.environ.get("E2E_TEST_CONCURRENT_USERS", "100"):
            try:
                config.test_concurrent_users = int(os.environ["E2E_TEST_CONCURRENT_USERS"])
            except ValueError:
                pass
        
        return config
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return {
            "test_mode": self.test_mode,
            "debug_mode": self.debug_mode,
            "test_db_path": self.test_db_path,
            "test_db_url": self.test_db_url,
            "ws_test_timeout": self.ws_test_timeout,
            "ws_test_reconnect_delay": self.ws_test_reconnect_delay,
            "ws_test_max_reconnects": self.ws_test_max_reconnects,
            "message_test_batch_size": self.message_test_batch_size,
            "message_test_chunk_size": self.message_test_chunk_size,
            "test_rate_limit_per_minute": self.test_rate_limit_per_minute,
            "test_concurrent_users": self.test_concurrent_users,
            "cleanup_on_finish": self.cleanup_on_finish,
            "cleanup_timeout": self.cleanup_timeout,
            "mock_llm_enabled": self.mock_llm_enabled,
            "mock_vector_store_enabled": self.mock_vector_store_enabled,
            "mock_webhook_enabled": self.mock_webhook_enabled,
            "use_mock_data": self.use_mock_data,
            "data_seed_limit": self.data_seed_limit,
        }