import unittest
from services import process_message_and_get_response

class TestChatLogic(unittest.TestCase):

    def test_basic_greeting(self):
        # Test case for simple greeting
        message = "Xin chào, bạn có thể giúp tôi được không?"
        response = process_message_and_get_response(message, history=[])
        self.assertTrue("Chào bạn" in response or "Tôi sẵn sàng" in response)

    def test_greeting_with_context(self):
        # Test case for a follow-up question based on history
        history = [
            {"sender": "user", "message": "Tôi muốn tìm hiểu về lịch sử Hà Nội."},
            {"sender": "bot", "message": "Hà Nội có bề dày lịch sử hơn 2000 năm."}
        ]
        message = "Và điểm nổi bật nhất là gì?"
        response = process_message_and_get_response(message, history=history)
        self.assertTrue("Thời kỳ nào" in response or "Giai đoạn lịch sử" in response)

    def test_unsupported_topic(self):
        # Test case for topics outside the core knowledge base
        message = "Ai là thủ tướng hiện tại của quốc gia X?"
        response = process_message_and_get_response(message, history=[])
        self.assertTrue("Xin lỗi, tôi chưa có thông tin" in response or "Tôi không có đủ dữ liệu" in response)

    # Add more test cases here for specific features (e.g., product lookup, booking, etc.)

if __name__ == '__main__':
    unittest.main()