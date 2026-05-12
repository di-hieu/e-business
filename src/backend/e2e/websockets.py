"""
E2E WebSocket Handler for Testing

Provides WebSocket handling for E2E chat testing scenarios.
"""

import asyncio
import uuid
from typing import Dict, List, Optional, Callable, Any
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class TestMessage:
    """Test message for WebSocket testing."""
    id: str
    conversation_id: int
    role: str
    content: str
    metadata: Dict = field(default_factory=dict)
    timestamp: Optional[datetime] = None
    channel: str = "zalo"
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "conversation_id": self.conversation_id,
            "role": self.role,
            "content": self.content,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "channel": self.channel
        }


class E2EWebSocketHandler:
    """
    WebSocket handler for E2E testing.
    
    Provides mock WebSocket behavior for testing chat interactions
    without requiring actual WebSocket connections.
    """
    
    def __init__(
        self,
        timeout: float = 30.0,
        reconnect_delay: float = 2.0,
        max_reconnects: int = 5
    ):
        self.timeout = timeout
        self.reconnect_delay = reconnect_delay
        self.max_reconnects = max_reconnects
        self.conversations: Dict[int, Dict] = {}
        self.message_queues: Dict[str, List[Dict]] = {}
        self.handlers: Dict[str, List[Callable]] = {}
        
    async def on_message(
        self,
        conversation_id: int,
        message: TestMessage
    ) -> TestMessage:
        """Handle incoming test message."""
        
        # Store message
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = {
                "messages": [],
                "status": "active"
            }
        
        self.conversations[conversation_id]["messages"].append({
            "message": message.to_dict(),
            "timestamp": datetime.utcnow()
        })
        
        # Queue message for response
        queue_key = f"{conversation_id}_{message.role}"
        if queue_key not in self.message_queues:
            self.message_queues[queue_key] = []
        
        self.message_queues[queue_key].append(message)
        
        return message
    
    async def on_response(
        self,
        conversation_id: int,
        response_content: str,
        metadata: Optional[Dict] = None
    ) -> TestMessage:
        """Handle bot response generation."""
        
        queue_key = f"{conversation_id}_bot"
        if queue_key not in self.message_queues:
            return None
        
        # Find the last user message and pair with response
        if self.message_queues[queue_key]:
            message = self.message_queues[queue_key].pop(0)
            response = TestMessage(
                id=str(uuid.uuid4()),
                conversation_id=conversation_id,
                role="assistant",
                content=response_content,
                metadata=metadata or {}
            )
            
            # Add to conversation
            if conversation_id in self.conversations:
                self.conversations[conversation_id]["messages"].append({
                    "message": response.to_dict(),
                    "timestamp": datetime.utcnow()
                })
        
        return response
    
    async def stream_response(
        self,
        conversation_id: int,
        chunks: List[str],
        interval: float = 0.1
    ) -> List[TestMessage]:
        """Stream response in chunks (simulating streaming)."""
        
        messages = []
        for i, chunk in enumerate(chunks):
            if self.message_queues.get(f"{conversation_id}_bot"):
                message = self.message_queues[f"{conversation_id}_bot"].pop(0)
                response = TestMessage(
                    id=str(uuid.uuid4()),
                    conversation_id=conversation_id,
                    role="assistant",
                    content=chunk,
                    metadata=message.metadata
                )
                messages.append(response)
                await asyncio.sleep(interval)
        
        return messages
    
    def register_handler(
        self,
        key: str,
        handler: Callable
    ) -> None:
        """Register a message handler."""
        if key not in self.handlers:
            self.handlers[key] = []
        self.handlers[key].append(handler)
    
    def handle_tool_call(
        self,
        conversation_id: int,
        tool_name: str,
        tool_params: Dict,
        result: Any
    ) -> TestMessage:
        """Handle tool call execution."""
        
        if self.message_queues.get(f"{conversation_id}_bot"):
            message = self.message_queues[f"{conversation_id}_bot"].pop(0)
            metadata = {
                "tool_name": tool_name,
                "tool_params": tool_params,
                "tool_result": result,
                "tool_status": "success"
            }
            
            if conversation_id in self.conversations:
                self.conversations[conversation_id]["messages"].append({
                    "message": message.to_dict(),
                    "timestamp": datetime.utcnow()
                })
        
        return message
    
    def get_conversation_messages(
        self,
        conversation_id: int
    ) -> List[Dict]:
        """Get all messages for a conversation."""
        return self.conversations.get(conversation_id, {}).get("messages", [])
    
    async def close_connection(self) -> None:
        """Clean up test connections."""
        self.conversations.clear()
        self.message_queues.clear()
        self.handlers.clear()
    
    def __repr__(self) -> str:
        return f"E2EWebSocketHandler(conversations={len(self.conversations)})"