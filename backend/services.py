#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import requests
from datetime import datetime

# --- Configuration ---
OLLAMA_API_URL = os.environ.get('OLLAMA_API_URL', 'http://localhost:11434/api/chat')
OLLAMA_MODEL = os.environ.get('OLLAMA_MODEL', 'llama2')

# NOTE: Knowledge base structures (FAQS, Products) should ideally be loaded from a centralized config or database.
# For now, we simulate loading the structure from the original knowledgeBase JS object.
# In a production Python environment, this would involve a proper data loading mechanism.
class KnowledgeBase:
    def __init__(self):
        # Placeholder data mirroring the structure required by the original JS logic
        self.faqs = [
            {"keywords": ["giờ mở cửa", "mua hàng"], "answer": "Chúng tôi mở cửa từ 8h sáng đến 10h tối hàng ngày."},
            {"keywords": ["giao hàng", "ship"], "answer": "Chúng tôi giao hàng toàn quốc, mất khoảng 3-5 ngày làm việc tùy khu vực."}
        ]
        self.products = [
            {"name": "Áo Thun Cá Tính", "sku": "AT001", "description": "Áo thun chất liệu cotton cao cấp, nhiều màu sắc.", "price": "250.000"},
            {"name": "Quần Jeans Slim", "sku": "QJ002", "description": "Quần jeans co giãn, phù hợp với nhiều dịp.", "price": "450.000"}
        ]

KNOWLEDGE_BASE = KnowledgeBase()


def retrieve_knowledge(message_text):
    """
    Searches the local knowledge base for relevant FAQs or products.
    :param message_text: The user's input.
    :return: Contextual information found.
    """
    lower_case_message = message_text.lower()
    context = []
    
    # Search FAQs
    faq_match = next((faq for faq in KNOWLEDGE_BASE.faqs if any(keyword in lower_case_message for keyword in faq['keywords'])), None)
    if faq_match:
        context.append("[FAQ]: %s" % faq_match['answer'])
    
    # Search Products
    product_match = next((product for product in KNOWLEDGE_BASE.products if any(keyword in lower_case_message for keyword in product['keywords'])), None)
    if product_match:
        context.append("[PRODUCT]: %s (SKU: %s) - %s | Giá: %s" % (
            product_match['name'], 
            product_match['sku'], 
            product_match['description'], 
            product_match['price']
        ))
    
    if context:
        return "[Knowledge Context Found]: " + "\n---\n".join(context)
    
    return "Không tìm thấy thông tin cụ thể trong cơ sở dữ liệu nội bộ. Hãy hỏi về các chủ đề chung để tôi tra cứu thêm."


def process_chat_request(message_text, sender_id, platform):
    """
    Main function to process a user's message through the AI core.
    :param message_text: The incoming text message from the user.
    :param sender_id: ID of the sender.
    :param platform: Platform of the message (Facebook, Zalo, etc.).
    :return: The AI-generated, formatted response text.
    """
    # 1. Retrieve and inject context/knowledge base
    knowledge_context = retrieve_knowledge(message_text)
    
    if not OLLAMA_API_URL:
        print("WARNING: OLLAMA_API_URL not set. Cannot connect to AI service.")
        return "Xin chào! Tôi là trợ lý AI của cửa hàng. Hiện tại tôi đang gặp sự cố kỹ thuật và không thể trả lời bạn. Vui lòng thử lại sau. (Platform: %s)" % platform

    print("\n--- Running AI processing for %s ---" % platform)

    # 2. Construct the system prompt using the retrieved knowledge
    system_prompt = ("Bạn là một trợ lý AI bán hàng chuyên nghiệp, thân thiện, và hiểu rõ về thương mại xã hội tại Việt Nam. Nhiệm vụ của bạn là sử dụng thông tin CUNG CẤP TRONG TRUYỀN THÔNG BỐI CẢNH bên dưới để trả lời câu hỏi của khách hàng một cách chính xác, đầy đủ, và mang tính chuyển đổi cao.\n\n"
                     "--- \n**BỐI CẢNH TRI THỨC:**\n%s\n---\n\n"
                     "Các bước trả lời cần tuân theo:\n"
                     "1. Phân tích ý định của khách hàng.\n"
                     "2. Nếu thông tin có trong BỐI CẢNH, hãy sử dụng nó để trả lời.\n"
                     "3. Nếu không có thông tin, hãy trả lời một cách tự nhiên và lịch sự, đồng thời gợi ý khách hàng cung cấp thêm chi tiết.\n"
                     "4. Luôn kết thúc bằng lời kêu gọi hành động (CTA) như \"Vui lòng để lại SĐT/Địa chỉ để được tư vấn chi tiết hơn.\""
                    ) % knowledge_context
    
    # 3. Construct the payload for the LLM API
    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message_text}
        ],
        "temperature": 0.7
    }
    
    try:
        # 4. Call the Ollama API using requests
        response = requests.post(
            OLLAMA_API_URL, 
            json=payload, 
            headers={'Content-Type': 'application/json'}
        )
        response.raise_for_status() # Raises HTTPError for bad status codes (4xx or 5xx)
        
        response_data = response.json()
        ai_response = response_data['choices'][0]['message']['content']
        
        # 5. Further process/format response
        return format_ai_response(ai_response, platform)
    except requests.exceptions.HTTPError as http_error:
        print("HTTP Error calling Ollama API: %s" % http_error)
        return "Xin lỗi, hệ thống AI trả về lỗi HTTP: %s. Vui lòng kiểm tra kết nối máy chủ AI." % http_error.response.status_code
    except requests.exceptions.ConnectionError:
        print("Connection Error calling Ollama API.")
        return "Xin lỗi, tôi đã gặp lỗi khi kết nối với hệ thống AI (Connection Error). Vui lòng kiểm tra xem dịch vụ AI có đang chạy không."
    except Exception as e:
        print("General Error calling Ollama API: %s" % e)
        return "Xin lỗi, tôi đã gặp một lỗi không xác định khi xử lý yêu cầu AI. Vui lòng liên hệ trực tiếp với nhân viên hỗ trợ."


def format_ai_response(raw_response, platform):
    """
    Formats the raw AI response to ensure consistency and actionability.
    """
    formatted = raw_response.strip()
    
    # Simple check for a follow-up action
    if "hàng" in formatted.lower() and "Xin lỗi" not in formatted:
        formatted = "\n🛒 **Gợi ý hành động:** Bạn có thể xem qua các sản phẩm X và Y, chúng phù hợp với yêu cầu của bạn.\n"
    
    return formatted