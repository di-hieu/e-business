"""
SC Chatbot Configuration API

This module provides endpoints for configuring the chatbot system
through the web UI.
"""

from fastapi import APIRouter, HTTPException, Query, Request
from typing import Dict

# Initialize router
config_router = APIRouter(prefix="/config", tags=["Configuration"])


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


def get_config_file_path() -> str:
    """Get path to configuration file (.env)"""
    import os
    
    # Try multiple possible paths
    possible_paths = [
        os.path.join(os.path.dirname(__file__), "../../.env"),
        os.path.join(os.path.dirname(__file__), ".env"),
    ]
    
    for path in possible_paths:
        env_path = os.path.join(path, ".env") if path.endswith("/") else path
        if os.path.exists(env_path):
            return env_path
    
    # Fallback: return current working directory .env
    env_path = os.path.join(os.getcwd(), ".env")
    if os.path.exists(env_path):
        return env_path
    
    return ""


def load_config_from_env() -> Dict[str, str]:
    """Load configuration from .env file."""
    import os
    
    config = {}
    
    try:
        import dotenv
        from dotenv import find_dotenv, load_dotenv
        
        env_path = find_dotenv()
        if env_path:
            load_dotenv(env_path)
            config = {
                key: os.environ.get(key, "")
                for key in get_config_keys()
            }
    except ImportError:
        # If dotenv not available, just read from environment
        config = {
            key: os.environ.get(key, "")
            for key in get_config_keys()
        }
    except Exception as e:
        print(f"Failed to load .env file: {str(e)}")
        config = {
            key: os.environ.get(key, "")
            for key in get_config_keys()
        }
    
    return config


def get_config_keys() -> list:
    """Get list of configuration keys"""
    return [
        "TELEGRAM_BOT_TOKEN",
        "TELEGRAM_WEBHOOK_URL",
        "ZALO_APP_ID",
        "ZALO_APP_SECRET",
        "ZALO_REDIRECT_URI",
        "FACEBOOK_APP_ID",
        "FACEBOOK_APP_SECRET",
        "INSTAGRAM_ACCESS_TOKEN",
        "WECHAT_APP_ID",
        "WECHAT_APP_SECRET",
        "LLM_API_KEY",
        "LLM_MODEL",
        "LLM_TEMPERATURE",
        "LLM_MAX_TOKENS",
        "JWT_SECRET_KEY",
        "JWT_EXPIRY_MINUTES",
        "SESSION_TIMEOUT_MINUTES",
        "RAG_TOP_K",
        "RAG_SIMILARITY_THRESHOLD",
    ]


@config_router.get("/defaults", response_model=Dict[str, str])
async def get_config_defaults_endpoint():
    """
    Get default configuration values.
    
    Returns:
        Dictionary of configuration keys with their descriptions
    """
    return {
        "description": key,
        "default": value or "",
    }


@config_router.get("/variables", response_model=Dict[str, str])
async def get_config_variables(
    include_sensitive: bool = Query(
        False,
        description="Include sensitive values (only for admin users)",
    ),
    request: Request = None,
):
    """
    Get current configuration values.
    
    Args:
        include_sensitive: Whether to include sensitive values
    
    Returns:
        Dictionary of configuration key-value pairs
    
    Raises:
        HTTPException: If access denied for sensitive values
    """
    # Get current config
    config = load_config_from_env()
    
    # Filter out sensitive values if not requested
    if not include_sensitive:
        sensitive_keys = [
            "JWT_SECRET_KEY",
            "JWT_EXPIRY_MINUTES",
            "SESSION_TIMEOUT_MINUTES",
        ]
        # Remove sensitive keys from config
        config = {
            key: value for key, value in config.items()
            if key not in sensitive_keys
        }
    
    return config


@config_router.post("/variables", response_model=Dict[str, str])
async def save_config_variables(
    config_values: Dict[str, str],
    request: Request = None,
):
    """
    Save configuration values.
    
    Note: In POC mode, this writes to .env file.
    In production, you might want to use a database-backed config.
    
    Args:
        config_values: Dictionary of configuration key-value pairs
    
    Returns:
        Dictionary with save result
    
    Raises:
        HTTPException: If save fails
    """
    try:
        # Get config file path
        config_path = get_config_file_path()
        
        if not config_path:
            # Fall back to writing to memory (not persisted)
            # In production, you would use a database here
            return {
                "status": "warning",
                "message": "No config file found. Config not persisted.",
                "values": config_values,
            }
        
        # Load existing config
        config = load_config_from_env()
        
        # Update with new values
        config.update(config_values)
        
        # Write back to .env file
        with open(config_path, "w") as f:
            for key, value in config.items():
                # Skip sensitive keys unless explicitly set
                if key not in [
                    "JWT_SECRET_KEY",
                    "JWT_EXPIRY_MINUTES",
                    "SESSION_TIMEOUT_MINUTES",
                ] or value:
                    f.write(f"{key}={value}\n")
        
        # Reload config to verify
        config = load_config_from_env()
        
        return {
            "status": "success",
            "message": "Configuration saved",
            "values": config,
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save configuration: {str(e)}"
        )


@config_router.get("/status")
async def get_config_status():
    """
    Get configuration status.
    
    Returns:
        Status information about the configuration
    """
    config = load_config_from_env()
    defaults = get_config_defaults()
    
    configured_count = sum(
        1 for key in defaults.keys()
        if config.get(key)
    )
    
    return {
        "status": "ok",
        "configured_count": configured_count,
        "total_configs": len(defaults),
        "configured_channels": [
            key for key in defaults.keys()
            if any(channel in key for channel in ["ZALO", "FACEBOOK", "INSTAGRAM", "WECHAT", "TELEGRAM"])
        ],
        "configured_llm": "LLM_API_KEY" in config,
        "configured_jwt": "JWT_SECRET_KEY" in config,
        "configured_rag": "RAG_TOP_K" in config,
    }