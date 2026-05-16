from fastapi import APIRouter
from .auth import router as auth_router
from .chat import router as chat_router
from .knowledge import router as knowledge_router
from .tools import router as tools_router
from .app import config_router
from .admin import router as admin_router
from .webhooks import telegram_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(chat_router)
api_router.include_router(knowledge_router)
api_router.include_router(tools_router)
api_router.include_router(config_router)
api_router.include_router(admin_router)
# Include telegram_router (already has prefix="/webhooks" from webhooks.py)
from .webhooks import telegram_router
api_router.include_router(telegram_router)
# Include main webhooks router with empty prefix (webhooks.py already has prefix="/webhooks")
from .webhooks import router as webhooks_router
api_router.include_router(webhooks_router)
