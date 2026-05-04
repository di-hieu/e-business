// frontend/src/components/ChatBot.js
import React from 'react';

const ChatBot = ({ inputMessage, onInputChange, onSend, isLoading }) => {
    const handleSendClick = () => {
        onSend();
    };

    return (
        <div className="chat-input-container">
            <div className="input-group">
                <input
                    type="text"
                    placeholder="Nhập tin nhắn của bạn vào đây..."
                    value={inputMessage}
                    onChange={(e) => onInputChange(e.target.value)}
                    onKeyPress={(e) => {
                        if (e.key === 'Enter' && !isLoading) {
                            onSend();
                        }
                    }}
                    disabled={isLoading}
                />
                <button 
                    onClick={handleSendClick} 
                    disabled={!inputMessage.trim() || isLoading}
                    className="send-button"
                >
                    {isLoading ? 'Đang gửi...' : 'Gửi'}
                </button>
            </div>
        </div>
    );
};

export default ChatBot;