"""
SC Chatbot Configuration

Application settings and configuration management.
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""

    # =============================================================================
    # SECURITY
    # =============================================================================
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_EXPIRY_MINUTES: int = 30
    SESSION_TIMEOUT_MINUTES: int = 120

    # =============================================================================
    # LLM CONFIGURATION
    # =============================================================================
    LLM_API_KEY: Optional[str] = None
    LLM_MODEL: str = "gpt-4o-mini"
    LLM_TEMPERATURE: float = 0.7
    LLM_MAX_TOKENS: int = 2048

    # =============================================================================
    # EMBEDDING CONFIGURATION
    # =============================================================================
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    # =============================================================================
    # DATABASE CONFIGURATION
    # =============================================================================
    DATABASE_URL: str = "sqlite+aiosqlite:///./app.db"

    # =============================================================================
    # FAISS CONFIGURATION
    # =============================================================================
    FAISS_DIR: str = "./data/faiss"

    # =============================================================================
    # RATE LIMITING
    # =============================================================================
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60

    # =============================================================================
    # TELEGRAM CONFIGURATION
    # =============================================================================
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    TELEGRAM_WEBHOOK_URL: str = "https://your-domain.com/webhooks/telegram"
    TELEGRAM_VERIFICATION_TOKEN: Optional[str] = None
    TELEGRAM_INLINE_BOT_TOKEN: Optional[str] = None

    # =============================================================================
    # ZALO CONFIGURATION
    # =============================================================================
    ZALO_APP_ID: Optional[str] = None
    ZALO_APP_SECRET: Optional[str] = None
    ZALO_REDIRECT_URI: str = "http://localhost:8000/auth/zalo/callback"

    # =============================================================================
    # FACEBOOK CONFIGURATION
    # =============================================================================
    FACEBOOK_APP_ID: Optional[str] = None
    FACEBOOK_APP_SECRET: Optional[str] = None
    FACEBOOK_VERIFY_TOKEN: Optional[str] = None
    FACEBOOK_ACCESS_TOKEN: Optional[str] = None

    # =============================================================================
    # INSTAGRAM CONFIGURATION
    # =============================================================================
    INSTAGRAM_ACCESS_TOKEN: Optional[str] = None
    INSTAGRAM_APP_ID: Optional[str] = None
    INSTAGRAM_APP_SECRET: Optional[str] = None

    # =============================================================================
    # OPENROUTER CONFIGURATION
    # =============================================================================
    OPENROUTER_API_KEY: Optional[str] = None

    # =============================================================================
    # APPLICATION SETTINGS
    # =============================================================================
    HOSTNAME: str = "http://localhost:8000"
    DEBUG: bool = True

    # =============================================================================
    # TESTING
    # =============================================================================
    TEST_DB_PATH: str = "sqlite+aiosqlite:///./test_app.db"
    CLEANUP_ON_FINISH: bool = True

    # =============================================================================
    # TEST DATABASE PATH (for conftest)
    # =============================================================================
    test_db_path: str = TEST_DB_PATH

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()
