"""
SC Chatbot Tenant Model

Multi-tenant isolation model.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship


class Tenant:
    """Represents a multi-tenant workspace."""
    
    __tablename__ = "tenants"
    
    id = Column(Integer, primary_key=True, index=True, comment="Tenant ID")
    tenant_key = Column(String(50), unique=True, index=True, comment="Unique tenant identifier")
    name = Column(String(100), nullable=False, comment="Tenant/company name")
    api_key = Column(String(255), unique=True, nullable=False, comment="Tenant API key")
    
    # Settings
    llm_model = Column(String(50), default="gpt-4o-mini", comment="LLM model to use")
    response_style = Column(String(50), default="professional", comment="Response style: professional, casual, friendly")
    language = Column(String(10), default="en", comment="Default language code")
    
    # Quota management
    token_limit = Column(Integer, default=1000, comment="Monthly token limit")
    message_limit = Column(Integer, default=100, comment="Daily message limit")
    is_active = Column(Boolean, default=True, comment="Tenant status")
    
    # Timestamps
    created_at = Column(DateTime, default=lambda: __import__('datetime').datetime.utcnow())
    updated_at = Column(DateTime, default=lambda: __import__('datetime').datetime.utcnow(), onupdate=lambda: __import__('datetime').datetime.utcnow())
    
    # Relationships (lazy loading to avoid circular imports)
    users = relationship("User", back_populates="tenant", cascade="all, delete-orphan", lazy="dynamic")
    conversations = relationship("Conversation", back_populates="tenant", cascade="all, delete-orphan", lazy="dynamic")
    knowledge_docs = relationship("KnowledgeDocument", back_populates="tenant", cascade="all, delete-orphan", lazy="dynamic")
    tools = relationship("ToolDefinition", back_populates="tenant", cascade="all, delete-orphan", lazy="dynamic")
    chat_sessions = relationship("ChatSession", back_populates="tenant", cascade="all, delete-orphan", lazy="dynamic")
    
    def __init__(self, tenant_key: str, name: str, api_key: str, 
                 llm_model: str = "gpt-4o-mini", response_style: str = "professional",
                 language: str = "en", token_limit: int = 1000, message_limit: int = 100):
        self.tenant_key = tenant_key
        self.name = name
        self.api_key = api_key
        self.llm_model = llm_model
        self.response_style = response_style
        self.language = language
        self.token_limit = token_limit
        self.message_limit = message_limit
        self.is_active = True

    def to_dict(self):
        """Convert to dictionary."""
        return {
            "id": self.id,
            "tenant_key": self.tenant_key,
            "name": self.name,
            "api_key": self.api_key,
            "llm_model": self.llm_model,
            "response_style": self.response_style,
            "language": self.language,
            "token_limit": self.token_limit,
            "message_limit": self.message_limit,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def __repr__(self):
        return f"<Tenant(tenant_key='{self.tenant_key}', name='{self.name}')>"


class ChannelConfig:
    """Represents channel configuration for a tenant."""

    __tablename__ = "channel_configs"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False)
    channel = Column(String(50), nullable=False, comment="Channel: zalo, telegram, facebook, instagram")

    # Zalo config
    zalo_app_id = Column(String(100), nullable=True)
    zalo_app_secret = Column(String(255), nullable=True)
    zalo_redirect_uri = Column(String(255), nullable=True)

    # Telegram config
    telegram_bot_token = Column(String(255), nullable=True)
    telegram_webhook_url = Column(String(255), nullable=True)
    telegram_verification_token = Column(String(100), nullable=True)
    telegram_inline_bot_token = Column(String(255), nullable=True)

    # Facebook config
    facebook_app_id = Column(String(100), nullable=True)
    facebook_app_secret = Column(String(255), nullable=True)
    facebook_verify_token = Column(String(100), nullable=True)
    facebook_access_token = Column(String(255), nullable=True)

    # Instagram config
    instagram_access_token = Column(String(255), nullable=True)
    instagram_app_id = Column(String(100), nullable=True)
    instagram_app_secret = Column(String(255), nullable=True)

    # Status
    is_active = Column(Boolean, default=False, comment="Whether channel is active")
    is_connected = Column(Boolean, default=False, comment="Whether channel is connected")

    # Timestamps
    created_at = Column(DateTime, default=lambda: __import__('datetime').datetime.utcnow())
    updated_at = Column(DateTime, default=lambda: __import__('datetime').datetime.utcnow(), onupdate=lambda: __import__('datetime').datetime.utcnow())

    def __init__(self, tenant_id: int, channel: str, **kwargs):
        self.tenant_id = tenant_id
        self.channel = channel
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def to_dict(self):
        """Convert to dictionary."""
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "channel": self.channel,
            "zalo_app_id": self.zalo_app_id,
            "zalo_app_secret": self.zalo_app_secret,
            "zalo_redirect_uri": self.zalo_redirect_uri,
            "telegram_bot_token": self.telegram_bot_token,
            "telegram_webhook_url": self.telegram_webhook_url,
            "telegram_verification_token": self.telegram_verification_token,
            "telegram_inline_bot_token": self.telegram_inline_bot_token,
            "facebook_app_id": self.facebook_app_id,
            "facebook_app_secret": self.facebook_app_secret,
            "facebook_verify_token": self.facebook_verify_token,
            "facebook_access_token": self.facebook_access_token,
            "instagram_access_token": self.instagram_access_token,
            "instagram_app_id": self.instagram_app_id,
            "instagram_app_secret": self.instagram_app_secret,
            "is_active": self.is_active,
            "is_connected": self.is_connected,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def __repr__(self):
        return f"<ChannelConfig(id={self.id}, channel='{self.channel}')>"