"""
SC Chatbot Database Connection

Database connection setup using SQLAlchemy with aiosqlite.
"""

import sys
import os

# Add backend root to path for absolute imports
backend_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if backend_root not in sys.path:
    sys.path.insert(0, backend_root)

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from contextlib import asynccontextmanager


engine = create_engine(
    "sqlite+aiosqlite:///./app.db",
    echo=False,
    connect_args={"check_same_thread": False},
)

Base = declarative_base()


async def init_db():
    """Initialize database tables and import models."""
    from .tenant import Tenant
    from .user import User
    from .conversation import Conversation
    from .message import Message
    from .knowledge import KnowledgeDocument
    from .tool import ToolDefinition
    from .chat_session import ChatSession
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def get_db_session():
    """Get database session context manager."""
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session


async def create_all_tables():
    """Create all database tables."""
    await init_db()


async def drop_all_tables():
    """Drop all database tables."""
    from .tenant import Tenant
    from .user import User
    from .conversation import Conversation
    from .message import Message
    from .knowledge import KnowledgeDocument
    from .tool import ToolDefinition
    from .chat_session import ChatSession
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)