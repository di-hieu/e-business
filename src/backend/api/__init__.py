"""
SC Chatbot API Routes

Main API router for the chatbot platform.
"""

from fastapi import APIRouter
from .auth import router as auth_router
from .chat import router as chat_router
from .knowledge import router as knowledge_router
from .tools import router as tools_router
from .app import config_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(chat_router)
api_router.include_router(knowledge_router)
api_router.include_router(tools_router)
api_router.include_router(config_router)