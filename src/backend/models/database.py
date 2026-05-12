"""
SC Chatbot Database Connection

Database connection setup using SQLAlchemy with aiosqlite.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from contextlib import asynccontextmanager

from .tenant import Tenant
from .user import User
from .conversation import Conversation
from .message import Message
from .knowledge import KnowledgeDocument
from .tool import ToolDefinition
from .chat_session import ChatSession


@asynccontextmanager
async def get_db_session():
    """Get database session context manager."""
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session


engine = create_engine(
    "sqlite+aiosqlite:///./app.db",
    echo=False,
    connect_args={"check_same_thread": False},
)

Base = declarative_base()


async def init_db():
    """Initialize database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)