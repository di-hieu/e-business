"""
SC Chatbot Auth Endpoints

Authentication and registration API endpoints.
"""

import sys
import os

# Add backend parent to path
backend_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_root not in sys.path:
    sys.path.insert(0, backend_root)

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr

# Import from top-level
import models.database as db_model
import services.auth_service as auth_service
import services.tool_service as tool_service

router = APIRouter(prefix="/auth", tags=["Authentication"])


class TenantRegistration(BaseModel):
    """Tenant registration request."""
    tenant_key: str
    email: EmailStr
    password: str
    name: str


class LoginRequest(BaseModel):
    """Login request."""
    tenant_key: str
    email: EmailStr
    password: str


class RefreshTokenRequest(BaseModel):
    """Refresh token request."""
    refresh_token: str


class UserResponse(BaseModel):
    """User response model."""
    id: str
    email: str
    role: str
    tenant_key: str
    access_token: str
    refresh_token: str


@router.post("/register", response_model=UserResponse)
async def register_tenant(data: TenantRegistration):
    """Register a new tenant and create admin user."""
    result = auth_service.create_tenant(
        tenant_key=data.tenant_key,
        email=data.email,
        password=data.password,
        name=data.name,
    )
    return result


@router.post("/login", response_model=UserResponse)
async def login(data: LoginRequest):
    """Authenticate user and return tokens."""
    result = auth_service.authenticate_user(
        tenant_key=data.tenant_key,
        email=data.email,
        password=data.password,
    )
    if not result:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return result


@router.post("/refresh", response_model=UserResponse)
async def refresh_token(data: RefreshTokenRequest):
    """Refresh access token."""
    payload = auth_service.verify_token(data.refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    return {
        "sub": payload.get("sub"),
        "email": payload.get("email"),
        "tenant_id": payload.get("tenant_id"),
        "tenant_key": payload.get("tenant_key"),
        "role": payload.get("role"),
        "access_token": auth_service.create_access_token(payload),
        "refresh_token": auth_service.create_refresh_token(payload),
    }


@router.get("/me")
async def get_current_user():
    """Get current user info - simplified for POC."""
    return {
        "email": "admin@example.com",
        "role": "admin",
        "tenant_key": "default",
    }