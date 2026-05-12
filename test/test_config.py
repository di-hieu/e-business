# Test Configuration for SC Chatbot E2E Testing

"""
Test configuration module for the SC Chatbot project.
Contains test environment variables, settings, and utilities.
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent
TEST_DIR = BASE_DIR / "test"

# Test Environment Variables
TEST_ENV = {
    # Application settings
    "TEST_MODE": True,
    "DEBUG": True,
    
    # Database settings (use separate test DB)
    "TEST_DATABASE_URL": os.getenv(
        "TEST_DATABASE_URL",
        "sqlite:///test_test.db"
    ),
    "TEST_POSTGRES_USER": os.getenv("TEST_POSTGRES_USER", "testuser"),
    "TEST_POSTGRES_PASSWORD": os.getenv("TEST_POSTGRES_PASSWORD", "testpass"),
    "TEST_POSTGRES_HOST": os.getenv("TEST_POSTGRES_HOST", "localhost"),
    "TEST_POSTGRES_PORT": os.getenv("TEST_POSTGRES_PORT", "5432"),
    "TEST_POSTGRES_DATABASE": os.getenv("TEST_POSTGRES_DATABASE", "test_scc"),
    
    # Redis for caching (test instance)
    "TEST_REDIS_URL": os.getenv("TEST_REDIS_URL", "redis://localhost:6379/1"),
    
    # API Keys (use mocks in test mode)
    "TEST_ZALO_CLIENT_ID": os.getenv("TEST_ZALO_CLIENT_ID", "test_zalo_client_id"),
    "TEST_ZALO_CLIENT_SECRET": os.getenv("TEST_ZALO_CLIENT_SECRET", "test_zalo_secret"),
    "TEST_ZALO_WEBHOOK_URL": os.getenv("TEST_ZALO_WEBHOOK_URL", "http://localhost:8000/webhooks/zalo"),
    
    "TEST_FACEBOOK_APP_ID": os.getenv("TEST_FACEBOOK_APP_ID", "test_fb_app_id"),
    "TEST_FACEBOOK_APP_SECRET": os.getenv("TEST_FACEBOOK_APP_SECRET", "test_fb_secret"),
    "TEST_FACEBOOK_PAGE_ID": os.getenv("TEST_FACEBOOK_PAGE_ID", "test_fb_page_id"),
    
    "TEST_INSTAGRAM_CLIENT_ID": os.getenv("TEST_INSTAGRAM_CLIENT_ID", "test_ig_client_id"),
    "TEST_INSTAGRAM_CLIENT_SECRET": os.getenv("TEST_INSTAGRAM_CLIENT_SECRET", "test_ig_secret"),
    "TEST_INSTAGRAM_USER_ACCESS_TOKEN": os.getenv("TEST_INSTAGRAM_USER_ACCESS_TOKEN", "test_ig_token"),
    
    # LLM settings (use mock in tests)
    "TEST_LLM_PROVIDER": os.getenv("TEST_LLM_PROVIDER", "mock"),
    "TEST_LLM_API_KEY": os.getenv("TEST_LLM_API_KEY", "test_llm_api_key"),
    
    # Vector DB settings
    "TEST_VECTOR_DB_PATH": os.getenv(
        "TEST_VECTOR_DB_PATH",
        str(TEST_DIR / "data" / "test_embeddings.faiss")
    ),
    
    # Test timeouts
    "TEST_TIMEOUT": int(os.getenv("TEST_TIMEOUT", "30")),
    "TEST_WAIT_TIME": int(os.getenv("TEST_WAIT_TIME", "1000")),
    
    # Rate limits for tests
    "TEST_RATE_LIMIT_PER_MINUTE": int(os.getenv("TEST_RATE_LIMIT_PER_MINUTE", "100")),
}

# Test fixtures paths
FIXTURES_DIR = TEST_DIR / "fixtures"
TEST_DATA_DIR = FIXTURES_DIR / "data"
MOCK_FILES_DIR = FIXTURES_DIR / "mocks"

# Browser configurations for Playwright
BROWSER_CONFIG = {
    "chromium": {"timeout": 30000, "retry": 30000},
    "firefox": {"timeout": 30000, "retry": 30000},
    "webkit": {"timeout": 30000, "retry": 30000},
}

# Test scenarios configuration
TEST_SCENARIOS = {
    "channel_message": {
        "enabled": True,
        "rate_limit": 10,  # messages per minute in tests
    },
    "rag_retrieval": {
        "enabled": True,
        "num_queries": 5,
    },
    "tool_calling": {
        "enabled": True,
        "num_tools": 3,
    },
    "multi_tenant": {
        "enabled": True,
        "num_tenants": 5,
    },
}

# Coverage settings
COVERAGE_SETTINGS = {
    "branch": True,
    "lines": True,
    "functions": True,
    "statements": True,
    "exclude": [
        "**/test_*",
        "**/__pycache__",
        "**/conftest.py",
        "**/mocks/*",
    ],
}

# Generate environment variables as shell commands
def get_test_env_script():
    """Generate bash script for test environment variables."""
    lines = ["#!/bin/bash", "# Test Environment Variables", ""]
    
    for key, value in TEST_ENV.items():
        if isinstance(value, str) and value.startswith("http"):
            value = f'"{value}"'
        lines.append(f'export {key}={value}')
    
    return "\n".join(lines)

if __name__ == "__main__":
    print("Test Configuration")
    print(f"Test Directory: {TEST_DIR}")
    print(f"Fixtures Directory: {FIXTURES_DIR}")
    print(f"Test Database: {TEST_ENV['TEST_DATABASE_URL']}")
    print(f"LLM Provider: {TEST_ENV['TEST_LLM_PROVIDER']}")