"""
SC Chatbot Auth Endpoints

Authentication and registration API endpoints.
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel, EmailStr
from typing import Optional

from ..services.auth_service import AuthService

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
    result = AuthService.create_tenant(
        tenant_key=data.tenant_key,
        email=data.email,
        password=data.password,
        name=data.name,
    )
    return result


@router.post("/login", response_model=UserResponse)
async def login(data: LoginRequest):
    """Authenticate user and return tokens."""
    result = AuthService.authenticate_user(
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
    payload = AuthService.verify_token(data.refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    return {
        "sub": payload.get("sub"),
        "email": payload.get("email"),
        "tenant_id": payload.get("tenant_id"),
        "tenant_key": payload.get("tenant_key"),
        "role": payload.get("role"),
        "access_token": AuthService.create_access_token(payload),
        "refresh_token": AuthService.create_refresh_token(payload),
    }


@router.get("/me")
async def get_current_user(token: str):
    """Get current user info."""
    payload = AuthService.verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return {
        "email": payload.get("email"),
        "role": payload.get("role"),
        "tenant_key": payload.get("tenant_key"),
    }