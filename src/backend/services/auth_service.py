"""
SC Chatbot Authentication Service

JWT-based authentication and authorization service.
"""

from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import jwt
import bcrypt
from functools import wraps

from ..models.tenant import Tenant
from ..models.user import User, UserRole


class AuthService:
    """Authentication service for SC Chatbot."""
    
    SECRET_KEY = "your-secret-key-here-change-in-production"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using bcrypt."""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode(), salt)
        return hashed.decode()
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash."""
        return bcrypt.checkpw(
            plain_password.encode(),
            hashed_password.encode(),
        )
    
    @staticmethod
    def create_access_token(data: Dict[str, Any]) -> str:
        """Create JWT access token."""
        to_encode = {
            "sub": data.get("sub", ""),
            "email": data.get("email", ""),
            "tenant_id": data.get("tenant_id", ""),
            "tenant_key": data.get("tenant_key", ""),
            "role": data.get("role", ""),
            "exp": datetime.utcnow() + timedelta(minutes=30),
        }
        return jwt.encode(to_encode, AuthService.SECRET_KEY, Algorithm=AuthService.ALGORITHM)
    
    @staticmethod
    def create_refresh_token(data: Dict[str, Any]) -> str:
        """Create JWT refresh token."""
        to_encode = {
            "sub": data.get("sub", ""),
            "email": data.get("email", ""),
            "tenant_id": data.get("tenant_id", ""),
            "tenant_key": data.get("tenant_key", ""),
            "role": data.get("role", ""),
            "exp": datetime.utcnow() + timedelta(days=7),
        }
        return jwt.encode(to_encode, AuthService.SECRET_KEY, Algorithm=AuthService.ALGORITHM)
    
    @staticmethod
    def verify_token(token: str) -> Optional[Dict[str, Any]]:
        """Verify JWT token and return payload."""
        try:
            payload = jwt.decode(token, AuthService.SECRET_KEY, algorithms=[AuthService.ALGORITHM])
            return {
                "sub": payload.get("sub"),
                "email": payload.get("email"),
                "tenant_id": payload.get("tenant_id"),
                "tenant_key": payload.get("tenant_key"),
                "role": payload.get("role"),
            }
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    @staticmethod
    def create_user(
        email: str,
        hashed_password: str,
        role: str = UserRole.AGENT.value,
        tenant_id: int = None,
    ) -> User:
        """Create a new user."""
        from ..models.user import User, UserRole as EnumRole
        
        user = User(
            email=email,
            hashed_password=hashed_password,
            role=EnumRole(role),
            tenant_id=tenant_id,
        )
        return user
    
    @staticmethod
    async def create_tenant(
        tenant_key: str,
        name: str,
        email: str,
        password: str,
    ) -> Dict[str, Any]:
        """Create a new tenant with initial admin user."""
        from ..models.tenant import Tenant
        from ..models.database import get_db_session
        
        # Generate API key
        import secrets
        api_key = secrets.token_urlsafe(32)
        
        # Create tenant
        tenant = Tenant(
            tenant_key=tenant_key.lower(),
            name=name,
            api_key=api_key,
        )
        
        # Hash password
        hashed_pw = AuthService.hash_password(password)
        
        # Create admin user
        admin_user = AuthService.create_user(
            email=email,
            hashed_password=hashed_pw,
            role=UserRole.ADMIN.value,
            tenant_id=tenant.id,
        )
        
        async with get_db_session() as session:
            session.add(tenant)
            session.add(admin_user)
            session.commit()
        
        return {
            "tenant_key": tenant.tenant_key,
            "api_key": api_key,
            "email": admin_user.email,
            "role": UserRole.ADMIN.value,
        }
    
    @staticmethod
    async def authenticate_user(
        tenant_key: str,
        email: str,
        password: str,
    ) -> Optional[Dict[str, Any]]:
        """Authenticate user and return token payload."""
        from ..models.tenant import Tenant
        from ..models.database import get_db_session
        
        # Get tenant
        async with get_db_session() as session:
            tenant = session.query(Tenant).filter(
                Tenant.tenant_key == tenant_key,
            ).first()
            
            if not tenant:
                return None
            
            # Find user
            user = session.query(User).filter(
                User.email == email,
                User.tenant_id == tenant.id,
            ).first()
            
            if not user or not AuthService.verify_password(password, user.hashed_password):
                return None
            
            return {
                "sub": str(user.id),
                "email": user.email,
                "tenant_id": str(tenant.id),
                "tenant_key": tenant.tenant_key,
                "role": user.role.value,
                "access_token": AuthService.create_access_token({
                    "sub": str(user.id),
                    "email": user.email,
                    "tenant_id": str(tenant.id),
                    "tenant_key": tenant.tenant_key,
                    "role": user.role.value,
                }),
                "refresh_token": AuthService.create_refresh_token({
                    "sub": str(user.id),
                    "email": user.email,
                    "tenant_id": str(tenant.id),
                    "tenant_key": tenant.tenant_key,
                    "role": user.role.value,
                }),
            }
    
    @staticmethod
    async def get_current_user(token: str) -> Optional[Dict[str, Any]]:
        """Get current user from token."""
        payload = AuthService.verify_token(token)
        if not payload:
            return None
        
        from ..models.tenant import Tenant
        from ..models.database import get_db_session
        
        async with get_db_session() as session:
            tenant = session.query(Tenant).filter(
                Tenant.tenant_key == payload.get("tenant_key"),
            ).first()
            
            if not tenant:
                return None
            
            return {
                "sub": payload.get("sub"),
                "email": payload.get("email"),
                "tenant_id": str(tenant.id),
                "tenant_key": tenant.tenant_key,
                "role": payload.get("role"),
            }