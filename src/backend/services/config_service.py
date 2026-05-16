"""
SC Chatbot - Configuration Service

Loads and manages application configuration from .env file.
"""

import os
from typing import Dict, Optional
from dotenv import load_dotenv, find_dotenv


# Global configuration cache
_config_cache: Dict[str, str] = {}


def get_config_defaults() -> Dict[str, str]:
    """Get default configuration keys and descriptions."""
    return {
        "TELEGRAM_BOT_TOKEN": "Telegram Bot token (required for Telegram integration)",
        "TELEGRAM_WEBHOOK_URL": "Telegram webhook URL (for production use)",
        "ZALO_APP_ID": "Zalo Official Account app ID",
        "ZALO_APP_SECRET": "Zalo Official Account app secret",
        "ZALO_REDIRECT_URI": "Zalo OAuth redirect URI",
        "FACEBOOK_APP_ID": "Facebook app ID",
        "FACEBOOK_APP_SECRET": "Facebook app secret",
        "INSTAGRAM_ACCESS_TOKEN": "Instagram access token",
        "WECHAT_APP_ID": "WeChat app ID",
        "WECHAT_APP_SECRET": "WeChat app secret",
        "LLM_API_KEY": "LLM API key (OpenAI/OpenRouter)",
        "LLM_MODEL": "LLM model name",
        "LLM_TEMPERATURE": "LLM temperature (0.0-2.0)",
        "LLM_MAX_TOKENS": "Maximum tokens for response",
        "JWT_SECRET_KEY": "JWT secret key for authentication",
        "JWT_EXPIRY_MINUTES": "JWT token expiry in minutes",
        "SESSION_TIMEOUT_MINUTES": "Session timeout in minutes",
        "RAG_TOP_K": "Number of top documents to retrieve",
        "RAG_SIMILARITY_THRESHOLD": "Similarity threshold for RAG",
    }


def get_config_from_env(key: str) -> str:
    """Get configuration value from environment variable."""
    value = os.environ.get(key, "")
    if value:
        _config_cache[key] = value
    return value


def get_config_from_api(key: str, tenant_key: str, auth_token: Optional[str] = None) -> str:
    """
    Get configuration value from API.
    
    This is used when configuration is managed via UI.
    Falls back to environment variable if API call fails.
    """
    try:
        # In production, this would make an HTTP request to /config/variables/{key}
        # For now, we check environment and cache
        if key in _config_cache:
            return _config_cache[key]
        
        # Fall back to environment variable
        value = get_config_from_env(key)
        _config_cache[key] = value
        return value
    except Exception as e:
        # Fall back to environment variable on error
        return get_config_from_env(key)


def set_config_in_cache(key: str, value: str):
    """Set configuration value in cache."""
    _config_cache[key] = value


def get_all_config() -> Dict[str, str]:
    """Get all configuration values."""
    defaults = get_config_defaults()
    config = {}
    
    for key, var in defaults.items():
        if key in _config_cache:
            config[key] = _config_cache[key]
        else:
            config[key] = get_config_from_env(key)
    
    return config


def get_config_value(key: str, tenant_key: str, auth_token: Optional[str] = None) -> str:
    """
    Get a single configuration value.
    
    Args:
        key: Configuration key (e.g., 'TELEGRAM_BOT_TOKEN')
        tenant_key: Tenant identifier
        auth_token: Authentication token (for sensitive configs)
    
    Returns:
        Configuration value or empty string
    """
    return get_config_from_api(key, tenant_key, auth_token)


def get_sensitive_config_value(key: str, auth_token: str) -> Optional[str]:
    """
    Get sensitive configuration value.
    
    Args:
        key: Configuration key
        auth_token: User's authentication token
    
    Returns:
        Configuration value or None if not allowed
    """
    # For sensitive configs, only allow admin users to access
    user_info = _verify_token(auth_token)
    
    if not user_info or not user_info.get("role") == "admin":
        raise HTTPException(status_code=403, detail="Access denied to sensitive configuration")
    
    return get_config_from_api(key, "", auth_token)


def _verify_token(auth_token: str):
    """Verify JWT token and return user info."""
    from services.auth_service import AuthService
    return AuthService.verify_token(auth_token)


def load_config_from_file(file_path: str) -> Dict[str, str]:
    """
    Load configuration from .env file.
    
    Args:
        file_path: Path to .env file
    
    Returns:
        Dictionary of configuration key-value pairs
    """
    if os.path.exists(file_path):
        load_dotenv(file_path)
    
    return {
        key: os.environ.get(key, "")
        for key in get_config_defaults().keys()
    }


# Load initial config from .env
def init_config():
    """Initialize configuration cache from .env file"""
    global _config_cache
    
    # Find and load .env file
    env_path = find_dotenv()
    if env_path:
        load_dotenv(env_path)
    
    _config_cache = {
        key: os.environ.get(key, "")
        for key in get_config_defaults().keys()
    }


# Call init_config when module is imported
init_config()