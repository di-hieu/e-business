// frontend/src/App.js
import React, { useState, useEffect } from 'react';
import './App.css';
import ChatBot from './components/ChatBot';
import ChatHistory from './components/ChatHistory';
// Assume API endpoint is accessible via relative path or environment variable
const API_ENDPOINT = process.env.REACT_APP_API_ENDPOINT || 'http://localhost:3001/api/chat';

function App() {
    const [messages, setMessages] = useState([]);
    const [inputMessage, setInputMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    // Function to handle sending messages
    const sendMessage = async () => {
        if (!inputMessage.trim() || isLoading) return;

        const newMessage = { sender: 'user', text: inputMessage };
        setMessages(prev => [...prev, newMessage]);
        setInputMessage('');
        setIsLoading(true);

        try {
            const response = await fetch(API_ENDPOINT, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    senderId: 'user_session_id', // Placeholder for real session ID
                    messageText: inputMessage,
                    platform: 'web' // Specify the current client platform
                })
            });

            const data = await response.json();
            
            if (data.success) {
                const botMessage = { sender: 'bot', text: data.response };
                setMessages(prev => [...prev, botMessage]);
            } else {
                // Handle API errors
                const errorMessage = data.error || "Unknown API Error.";
                const errorMsg = { sender: 'bot', text: `[SYSTEM ERROR]: ${errorMessage}` };
                setMessages(prev => [...prev, errorMsg]);
            }
        } catch (error) {
            console.error("Network Error:", error);
            const errorMsg = { sender: 'bot', text: "Đã xảy ra lỗi kết nối mạng. Vui lòng kiểm tra lại server backend." };
            setMessages(prev => [...prev, errorMsg]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="App">
            <header>
                <h1>AI Chatbot Support</h1>
            </header>
            <div className="chat-container">
                <ChatHistory messages={messages} />
                <ChatBot 
                    inputMessage={inputMessage}
                    onInputChange={setInputMessage}
                    onSend={sendMessage}
                    isLoading={isLoading}
                />
            </div>
        </div>
    );
}

export default App;