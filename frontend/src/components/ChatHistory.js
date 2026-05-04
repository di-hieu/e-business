// frontend/src/components/ChatHistory.js
import React, { useRef, useEffect } from 'react';

const ChatHistory = ({ messages }) => {
    const chatContainerRef = useRef(null);

    // Effect to scroll to bottom whenever messages change
    useEffect(() => {
        if (chatContainerRef.current) {
            chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
        }
    }, [messages]);

    return (
        <div className="chat-history-container" ref={chatContainerRef}>
            {messages.length === 0 ? (
                <div className="welcome-message">
                    Chào mừng bạn đến với dịch vụ hỗ trợ AI. Hãy nhập câu hỏi của bạn bên dưới!
                </div>
            ) : (
                messages.map((message, index) => (
                    <div key={index} className={`message ${message.sender === 'user' ? 'user-message' : 'bot-message'}`}>
                        <p className="sender-name">{message.sender === 'user' ? 'Bạn' : 'Trợ lý AI'}</p>
                        <div className="message-text">{message.text}</div>
                    </div>
                ))
            )}
        </div>
    );
};

export default ChatHistory;