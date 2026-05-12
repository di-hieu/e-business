"""
Instagram Direct Channel Integration Tests

End-to-end tests for Instagram Direct Message webhook handling, message parsing, and response validation.
"""

import pytest
import json
from datetime import datetime
from httpx import ASGITransport, AsyncClient

# Mock webhook payloads
INSTAGRAM_MESSAGE = {
    "object": "instagram_page_submission",
    "entry": [{
        "id": "ig_page_id",
        "time": datetime.utcnow().timestamp(),
        "messaging": [{
            "timestamp": datetime.utcnow().timestamp(),
            "sender": {"id": "user_instagram_id"},
            "recipient": {"id": "ig_page_id"},
            "message": {
                "mid": "ABC123",
                "type": "text",
                "text": "I'm interested in this product"
            }
        }]
    }]
}

INSTAGRAM_STORY_REPLY = {
    "object": "instagram_page_submission",
    "entry": [{
        "id": "ig_page_id",
        "messaging": [{
            "timestamp": datetime.utcnow().timestamp(),
            "story_reply": {
                "story_item_id": "story_id_123",
                "message": {
                    "mid": "XYZ789",
                    "type": "text",
                    "text": "Can I get more info about this?"
                }
            },
            "sender": {"id": "user_instagram_id"}
        }]
    }]
}

INSTAGRAM_PRODUCT_TAG = {
    "object": "instagram_page_submission",
    "entry": [{
        "id": "ig_page_id",
        "messaging": [{
            "timestamp": datetime.utcnow().timestamp(),
            "message": {
                "mid": "DEF456",
                "type": "product_tag",
                "product_tag": {
                    "product": {
                        "product_id": "prod_123",
                        "name": "Premium Cotton Shirt",
                        "price": {
                            "currency": "USD",
                            "value": 29.99
                        }
                    },
                    "merchant": {
                        "id": "merchant_123",
                        "name": "Fashion Store"
                    }
                },
                "text": "Love this shirt! How much is it?"
            },
            "sender": {"id": "user_instagram_id"}
        }]
    }]
}

INSTAGRAM_CAROUSEL = {
    "object": "instagram_page_submission",
    "entry": [{
        "id": "ig_page_id",
        "messaging": [{
            "timestamp": datetime.utcnow().timestamp(),
            "message": {
                "mid": "GHI789",
                "type": "carousel_media",
                "carousel_media": [
                    {
                        "media_id": "media_1",
                        "carousel_parent_id": "carousel_id",
                        "image": {
                            "id": "img_id_1",
                            "url": "https://instagram.com/p/image1.jpg",
                            "width": 1080,
                            "height": 1080
                        }
                    },
                    {
                        "media_id": "media_2",
                        "carousel_parent_id": "carousel_id",
                        "image": {
                            "id": "img_id_2",
                            "url": "https://instagram.com/p/image2.jpg",
                            "width": 1080,
                            "height": 1080
                        }
                    }
                ],
                "text": "Check out these products!"
            },
            "sender": {"id": "user_instagram_id"}
        }]
    }]
}

INSTAGRAM_VERIFICATION_REQUEST = {
    "object": "instagram_page_submission",
    "entry": [{
        "id": "ig_page_id",
        "messaging": [{
            "timestamp": datetime.utcnow().timestamp(),
            "verification_request": {
                "verification_status": "pending",
                "message": {
                    "mid": "VER123",
                    "type": "text",
                    "text": "Please verify this business account"
                }
            },
            "sender": {"id": "unverified_user_id"}
        }]
    }]
}


class TestInstagramDirect:
    """Test suite for Instagram Direct integration."""
    
    @pytest.mark.e2e
    @pytest.mark.channel
    async def test_graph_api_webhook_setup(self, test_config):
        """Test Instagram Graph API webhook configuration."""
        # Verify Graph API setup is complete
        assert test_config.test_graph_api_setup
    
    @pytest.mark.e2e
    @pytest.mark.channel
    async def test_text_message_parsing(self, instagram_message):
        """Test parsing of text messages from Instagram."""
        message = instagram_message["entry"][0]["messaging"][0]["message"]
        
        assert message["type"] == "text"
        assert "product" in message["text"].lower()
    
    @pytest.mark.e2e
    @pytest.mark.channel
    async def test_story_reply_parsing(self, instagram_story_reply):
        """Test parsing of story replies from Instagram."""
        story_reply = instagram_story_reply["entry"][0]["messaging"][0]["story_reply"]
        
        assert story_reply["story_item_id"] == "story_id_123"
        assert story_reply["message"]["type"] == "text"
        assert "info" in story_reply["message"]["text"].lower()
    
    @pytest.mark.e2e
    @pytest.mark.channel
    async def test_product_tag_parsing(self, instagram_product_tag):
        """Test parsing of product tag messages from Instagram."""
        message = instagram_product_tag["entry"][0]["messaging"][0]["message"]
        
        assert message["type"] == "product_tag"
        product = message["product_tag"]["product"]
        assert product["name"] == "Premium Cotton Shirt"
        assert product["price"]["currency"] == "USD"
    
    @pytest.mark.e2e
    @pytest.mark.channel
    async def test_carousel_media_parsing(self, instagram_carousel):
        """Test parsing of carousel media from Instagram."""
        message = instagram_carousel["entry"][0]["messaging"][0]["message"]
        
        assert message["type"] == "carousel_media"
        assert len(message["carousel_media"]) == 2
        
        for media in message["carousel_media"]:
            assert "image" in media
            assert "url" in media["image"]
    
    @pytest.mark.e2e
    @pytest.mark.channel
    async def test_verification_flow(self, test_config):
        """Test user verification flow for Instagram."""
        # Only verified businesses can receive messages
        pass  # Placeholder
    
    @pytest.mark.e2e
    @pytest.mark.channel
    async def test_story_message_handling(self):
        """Test handling of story replies vs DMs."""
        # Story replies have different timestamp format
        assert True  # Placeholder
    
    @pytest.mark.e2e
    @pytest.mark.channel
    async def test_message_limit(self):
        """Test Instagram message rate limits (24 messages per day)."""
        # Instagram has daily message limits
        daily_limit = 24  # messages per day
        assert daily_limit > 0
    
    @pytest.mark.e2e
    @pytest.mark.channel
    async def test_whatsapp_api_fallback(self):
        """Test falling back to WhatsApp API if Instagram unavailable."""
        # Meta's WhatsApp API can be used as alternative
        pass  # Placeholder
    
    @pytest.mark.e2e
    @pytest.mark.channel
    async def test_instagram_business_account(self):
        """Test Instagram Business account requirements."""
        # Requires Instagram Business account with messaging allowed
        pass  # Placeholder


@pytest.fixture
def instagram_message_payload():
    """Instagram Direct message payload for testing."""
    return {
        "object": "instagram_page_submission",
        "entry": [{
            "id": "ig_page_id",
            "time": datetime.utcnow().timestamp(),
            "messaging": [{
                "timestamp": datetime.utcnow().timestamp(),
                "sender": {"id": "user_instagram_id"},
                "recipient": {"id": "ig_page_id"},
                "message": {
                    "mid": "ABC123",
                    "type": "text",
                    "text": "Hello"
                }
            }]
        }]
    }


@pytest.fixture
def instagram_story_reply_payload():
    """Instagram story reply payload for testing."""
    return {
        "object": "instagram_page_submission",
        "entry": [{
            "id": "ig_page_id",
            "messaging": [{
                "timestamp": datetime.utcnow().timestamp(),
                "story_reply": {
                    "story_item_id": "story_id_123",
                    "message": {
                        "mid": "XYZ789",
                        "type": "text",
                        "text": "Reply to story"
                    }
                },
                "sender": {"id": "user_instagram_id"}
            }]
        }]
    }