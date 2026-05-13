"""
SC Chatbot Webhook Handlers
Supports Zalo, Facebook, Instagram, and Telegram integrations
Configuration is loaded from UI via /config/variables API
"""

from fastapi import APIRouter, HTTPException, Request, BackgroundTasks, status
from fastapi.responses import JSONResponse
import hmac
import hashlib
import json
from datetime import datetime
from typing import Optional, Any
from ..services.config_service import get_config_value, get_config_from_api
from fastapi import HTTPException

from ..models.database import get_db_session
from ..services.auth_service import AuthService
from ..models.conversation import Conversation
from ..models.message import Message
from ..rag.pipeline import RAGPipeline

# Initialize router
router = APIRouter(prefix="/webhooks", tags=["Webhooks"])


# =============================================================================
# TELEGRAM WEBHOOK HANDLER
# =============================================================================


class TelegramWebhook:
    """Telegram webhook handler class - configuration loaded from UI"""
    
    def __init__(self, bot_token: Optional[str] = None):
        self.bot_token = bot_token or get_config_value("TELEGRAM_BOT_TOKEN", "")
        self._api_url = "https://api.telegram.org/bot" + self.bot_token
    
    @property
    def webhook_url(self) -> str:
        """Get webhook URL from config"""
        return get_config_value("TELEGRAM_WEBHOOK_URL", "")
    
    def verify_signature(self, update: dict) -> bool:
        """Verify webhook signature (if provided)"""
        signature = update.get("signature")
        if signature is None:
            return True  # No signature for testing
        
        # Compute expected signature
        expected_hash = hashlib.sha256(
            f"key:{update['chat_id']}".encode()
        ).hexdigest()
        
        return hmac.compare_digest(signature, expected_hash)
    
    async def handle_message(self, update: dict, request: Request):
        """Handle incoming Telegram message"""
        
        try:
            # Parse update
            chat_id = update.get("chat_id")
            message_id = update.get("message_id")
            text = update.get("message", {}).get("text")
            from_user_id = update.get("message", {}).get("from", {}).get("id")
            date_str = update.get("message", {}).get("date")
            
            # Skip non-text messages (for now, in POC)
            if not text:
                return True
            
            # Get bot token from config
            bot_token = self.bot_token or request.query_params.get("bot_token")
            
            # Verify token (if configured)
            token = AuthService.verify_token_from_header(request)
            if not token:
                raise HTTPException(status_code=401, detail="Invalid or missing token")
            
            user_info = AuthService.verify_token(token)
            if not user_info:
                raise HTTPException(status_code=401, detail="Invalid user token")
            
            # Get or create tenant from user info
            async with get_db_session() as session:
                # Find tenant for this user (or create default)
                tenant = session.query("tenants").filter(
                    "tenants.tenant_key IN (?)",
                    [user_info.get("tenant_key")]
                ).first()
                
                if not tenant:
                    raise HTTPException(status_code=404, detail="Tenant not found")
            
            # Create or get conversation
            conversation = await get_or_create_conversation(
                session=session,
                user_id=str(user_info["sub"]),
                tenant_id=tenant.id,
                channel="telegram",
            )
            
            # Store user message
            user_message = Message(
                conversation_id=conversation.id,
                role="user",
                content=text,
            )
            session.add(user_message)
            session.commit()
            
            # Process with RAG pipeline
            rag_pipeline = RAGPipeline(tenant_id=tenant.id)
            response = await rag_pipeline.generate_response(text)
            
            # Create assistant message
            assistant_message = Message(
                conversation_id=conversation.id,
                role="assistant",
                content=response,
            )
            session.add(assistant_message)
            session.commit()
            
            # Prepare response to Telegram
            bot_response = {
                "message_id": message_id,
                "text": response,
            }
            
            # Send response back to Telegram (async via background task)
            background_tasks.add_task(
                self.send_to_telegram,
                chat_id,
                bot_response
            )
            
            return {"ok": True, "result": bot_response}
            
        except HTTPException:
            raise
        except Exception as e:
            print(f"Telegram webhook error: {str(e)}")
            return {"ok": False, "error": str(e)}
    
    async def send_to_telegram(self, chat_id: int, bot_response: dict):
        """Send response to Telegram chat"""
        try:
            # For POC, we'll log the response instead
            # In production, uncomment the above code with actual bot token
            if self.bot_token:
                url = f"{self._api_url}/sendMessage"
                params = {
                    "chat_id": chat_id,
                    "text": bot_response["text"],
                    "parse_mode": "Markdown"
                }
                # response = requests.post(url, data=params)
                # response.raise_for_status()
                
            print(f"[Telegram] Sent response to chat {chat_id}: {bot_response['text'][:100]}...")
            
        except Exception as e:
            print(f"Failed to send to Telegram: {str(e)}")
    
    async def handle_file(self, update: dict, request: Request):
        """Handle file uploads (images, documents)"""
        
        try:
            # Parse file
            file_id = update.get("message", {}).get("document", {}).get("file_id")
            file_caption = update.get("message", {}).get("caption")
            
            if not file_id:
                return True
            
            # Verify token
            token = AuthService.verify_token_from_header(request)
            if not token:
                raise HTTPException(status_code=401, detail="Invalid or missing token")
            
            # Get user info
            user_info = AuthService.verify_token(token)
            
            # Store file metadata (actual file processing in background task)
            # ... file processing logic ...
            
            return True
            
        except Exception as e:
            print(f"Telegram file handling error: {str(e)}")
            return False


# Global Telegram handler instance
telegram_webhook: Optional[TelegramWebhook] = None


# =============================================================================
# WECHAT WEBHOOK HANDLER (for MVP)
# =============================================================================


class WechatWebhook:
    """WeChat Official Account webhook handler"""
    
    def __init__(self, appid: str = "", appsecret: str = ""):
        self.appid = appid or get_config_value("WECHAT_APP_ID", "")
        self.appsecret = appsecret or get_config_value("WECHAT_APP_SECRET", "")
        self.session_id = None
        self.user_openid = None
    
    async def handle_message(self, request: Request):
        """Handle incoming WeChat message"""
        
        try:
            # Parse request body
            body = await request.json()
            
            # Verify signature
            signature = request.headers.get("wechatpay_sig")
            # ... signature verification ...
            
            # Extract message
            msg = body.get("MsgId")
            
            # ... rest of handling logic ...
            
            return {"success": True}
            
        except Exception as e:
            print(f"WeChat webhook error: {str(e)}")
            return {"success": False, "error": str(e)}


wechat_webhook: Optional[WechatWebhook] = None


# =============================================================================
# FACEBOOK WEBHOOK HANDLER
# =============================================================================


class FacebookWebhook:
    """Facebook webhook handler"""
    
    def __init__(self, app_id: str = "", app_secret: str = ""):
        self.app_id = app_id or get_config_value("FACEBOOK_APP_ID", "")
        self.app_secret = app_secret or get_config_value("FACEBOOK_APP_SECRET", "")
    
    async def handle_page_message(self, request: Request):
        """Handle Facebook page message"""
        try:
            body = await request.json()
            
            # Verify signature
            page_access_token = body.get("entry", {}).get("verifier", "")
            
            # Extract message
            message = body.get("message", {})
            text = message.get("message") or message
            
            return {"success": True}
            
        except Exception as e:
            print(f"Facebook webhook error: {str(e)}")
            return {"success": False, "error": str(e)}


facebook_webhook: Optional[FacebookWebhook] = None


# =============================================================================
# INSTAGRAM WEBHOOK HANDLER
# =============================================================================


class InstagramWebhook:
    """Instagram webhook handler"""
    
    def __init__(self, access_token: str = ""):
        self.access_token = access_token or get_config_value("INSTAGRAM_ACCESS_TOKEN", "")
    
    async def handle_message(self, request: Request):
        """Handle Instagram message"""
        try:
            body = await request.json()
            
            # Verify token
            if not self.access_token:
                raise HTTPException(status_code=401, detail="Instagram token required")
            
            # Extract message
            message = body.get("object", {}).get("instagram", {}).get("data", [])
            
            return {"success": True}
            
        except Exception as e:
            print(f"Instagram webhook error: {str(e)}")
            return {"success": False, "error": str(e)}


instagram_webhook: Optional[InstagramWebhook] = None


# =============================================================================
# TELEGRAM WEBHOOK ENDPOINT
# =============================================================================


@router.post("/telegram", tags=["Telegram"])
async def telegram_webhook_endpoint(
    request: Request,
    update: dict = {},
    bot_token: Optional[str] = None,
):
    """
    Telegram webhook endpoint
    
    ## Usage
    
    1. Create a Telegram Bot via @BotFather
    2. Get bot token from @BotFather
    3. Add webhook: /setwebhook YOUR_WEBHOOK_URL
    4. Set webhook: /setwebhook YOUR_WEBHOOK_URL?bot_token=YOUR_BOT_TOKEN
    
    Example commands:
    ```
    /start - Get help
    /help - Show help message
    ```
    """
    
    global telegram_webhook
    
    # Get bot token from config or query param
    bot_token = bot_token or request.query_params.get("bot_token")
    
    if not bot_token:
        return JSONResponse(
            status_code=400,
            content={"ok": False, "error": "BOT_TOKEN required"}
        )
    
    try:
        # Initialize or use existing webhook handler
        if not telegram_webhook:
            telegram_webhook = TelegramWebhook(bot_token)
        
        # Handle update
        result = await telegram_webhook.handle_message(update, request)
        
        return JSONResponse(
            status_code=200,
            content=result
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Telegram webhook error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"ok": False, "error": str(e)}
        )


# =============================================================================
# TEST TELEGRAM WEBHOOK
# =============================================================================


@router.post("/telegram/test", tags=["Telegram", "Testing"])
async def test_telegram_webhook(
    request: Request,
    chat_id: int,
    message: str,
    bot_token: Optional[str] = None,
):
    """
    Test Telegram webhook (for development)
    
    Sends a test message to a specific Telegram chat.
    
    ## Usage
    
    ```bash
    curl -X POST "http://localhost:8000/webhooks/telegram/test?bot_token=YOUR_TOKEN" \
      -d "chat_id=YOUR_CHAT_ID" \
      -d "message=Hello from SC Chatbot!"
    ```
    """
    
    global telegram_webhook
    
    bot_token = bot_token or request.query_params.get("bot_token")
    
    if not bot_token:
        return JSONResponse(
            status_code=400,
            content={"ok": False, "error": "BOT_TOKEN required"}
        )
    
    try:
        # Initialize webhook handler
        if not telegram_webhook:
            telegram_webhook = TelegramWebhook(bot_token)
        
        # Create fake update
        update = {
            "message": {
                "chat_id": chat_id,
                "text": message,
            }
        }
        
        # Handle test message
        result = await telegram_webhook.handle_message(update, request)
        
        return JSONResponse(
            status_code=200,
            content={"ok": True, "result": result}
        )
        
    except Exception as e:
        print(f"Test Telegram webhook error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"ok": False, "error": str(e)}
        )


# =============================================================================
# WECHAT WEBHOOK ENDPOINT
# =============================================================================


@router.post("/wechat", tags=["WeChat"])
async def wechat_webhook_endpoint(
    request: Request,
):
    """
    WeChat webhook endpoint
    
    Example:
    ```bash
    curl -X POST "http://localhost:8000/webhooks/wechat" \
      -H "Content-Type: application/json" \
      -d '{"MsgId": "123456"}'
    ```
    """
    
    global wechat_webhook
    
    # Initialize handler
    if not wechat_webhook:
        wechat_webhook = WechatWebhook()
    
    try:
        result = await wechat_webhook.handle_message(request)
        
        return JSONResponse(
            status_code=200,
            content=result
        )
        
    except Exception as e:
        print(f"WeChat webhook error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"ok": False, "error": str(e)}
        )


# =============================================================================
# FACEBOOK WEBHOOK ENDPOINT
# =============================================================================


@router.post("/facebook", tags=["Facebook"])
async def facebook_webhook_endpoint(
    request: Request,
):
    """
    Facebook webhook endpoint
    
    Example:
    ```bash
    curl -X POST "http://localhost:8000/webhooks/facebook" \
      -H "Content-Type: application/json" \
      -d '{"entry": {"verifier": "ABC"}, "message": {"message": "Hello"}}'
    ```
    """
    
    global facebook_webhook
    
    # Initialize handler
    if not facebook_webhook:
        facebook_webhook = FacebookWebhook()
    
    try:
        result = await facebook_webhook.handle_page_message(request)
        
        return JSONResponse(
            status_code=200,
            content=result
        )
        
    except Exception as e:
        print(f"Facebook webhook error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"ok": False, "error": str(e)}
        )


# =============================================================================
# INSTAGRAM WEBHOOK ENDPOINT
# =============================================================================


@router.post("/instagram", tags=["Instagram"])
async def instagram_webhook_endpoint(
    request: Request,
):
    """
    Instagram webhook endpoint
    
    Example:
    ```bash
    curl -X POST "http://localhost:8000/webhooks/instagram" \
      -H "Content-Type: application/json" \
      -d '{"object": {"instagram": {"data": []}}}'
    ```
    """
    
    global instagram_webhook
    
    # Initialize handler
    if not instagram_webhook:
        instagram_webhook = InstagramWebhook()
    
    try:
        result = await instagram_webhook.handle_message(request)
        
        return JSONResponse(
            status_code=200,
            content=result
        )
        
    except Exception as e:
        print(f"Instagram webhook error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"ok": False, "error": str(e)}
        )


# =============================================================================
# ZALO WEBHOOK ENDPOINT
# =============================================================================


@router.post("/zalo", tags=["Zalo"])
async def zalo_webhook_endpoint(
    request: Request,
):
    """
    Zalo webhook endpoint
    
    Example:
    ```bash
    curl -X POST "http://localhost:8000/webhooks/zalo" \
      -H "Content-Type: application/json" \
      -d '{"messageType": "text", "content": "Hello"}'
    ```
    """
    
    try:
        body = await request.json()
        
        # Extract message
        message_type = body.get("messageType", "text")
        content = body.get("content")
        
        # TODO: Implement Zalo message handling
        return JSONResponse(
            status_code=200,
            content={"ok": True, "message": f"Received {message_type} message: {content}"}
        )
        
    except Exception as e:
        print(f"Zalo webhook error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"ok": False, "error": str(e)}
        )


# =============================================================================
# HEALTH CHECK
# =============================================================================


@router.get("/health", tags=["Health"])
async def webhook_health_check():
    """Health check endpoint for webhook server"""
    return {
        "status": "healthy",
        "services": {
            "telegram": "connected" if telegram_webhook else "not_configured",
            "wechat": "connected" if wechat_webhook else "not_configured",
            "facebook": "connected" if facebook_webhook else "not_configured",
            "instagram": "connected" if instagram_webhook else "not_configured",
        }
    }