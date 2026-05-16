"""
SC Chatbot Authentication Service

JWT token-based authentication for the chatbot platform.
"""

import sys
import os

# Add backend root to path for absolute imports
backend_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_root not in sys.path:
    sys.path.insert(0, backend_root)

import jwt
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict

import models.database as db_model
import models.user as user_model


# Get JWT settings from environment or use defaults
def get_jwt_settings():
    """Get JWT configuration."""
    secret = os.environ.get("JWT_SECRET_KEY", "your-secret-key-change-in-production")
    algorithm = os.environ.get("JWT_ALGORITHM", "HS256")
    expiration_minutes = int(os.environ.get("JWT_EXPIRY_MINUTES", 60))
    
    return {
        "secret": secret,
        "algorithm": algorithm,
        "expiration": timedelta(minutes=expiration_minutes),
    }


settings = get_jwt_settings()


def verify_token(token: str) -> Optional[Dict]:
    """
    Verify JWT token and decode claims.
    
    Args:
        token: JWT token to verify
    
    Returns:
        Dictionary of claims or None if invalid
    """
    try:
        payload = jwt.decode(
            token,
            settings["secret"],
            algorithms=[settings["algorithm"]]
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    except Exception:
        return None


def verify_token_from_header(request):
    """
    Extract and verify JWT token from Authorization header.
    
    Args:
        request: HTTP request object
    
    Returns:
        Decoded claims or None
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return None
    
    # Expect format: "Bearer <token>"
    try:
        parts = auth_header.split()
        if len(parts) != 2 or parts[0] != "Bearer":
            return None
        
        token = parts[1]
        return verify_token(token)
    except Exception:
        return None


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """
    Create JWT access token.
    
    Args:
        data: Claims to include in token
        expires_delta: Optional additional expiration time
    
    Returns:
        JWT token string
    """
    payload = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + settings["expiration"]
    
    payload.update({
        "exp": expire,
        "iat": datetime.utcnow(),
    })
    
    return jwt.encode(
        payload,
        settings["secret"],
        algorithm=settings["algorithm"]
    )


def create_refresh_token(
    data: dict,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """
    Create JWT refresh token (longer expiration).
    
    Args:
        data: Claims to include in token
        expires_delta: Optional additional expiration time
    
    Returns:
        JWT token string
    """
    payload = data.copy()
    
    # Refresh tokens typically last 7 days
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=7)
    
    payload.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh",
    })
    
    return jwt.encode(
        payload,
        settings["secret"],
        algorithm=settings["algorithm"]
    )