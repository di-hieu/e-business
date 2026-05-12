import { useEffect, useState } from 'react'
import { api } from '../api/client'

export default function ChatInterface({ onLogout }) {
  const [messages, setMessages] = useState([])
  const [inputText, setInputText] = useState('')
  const [loading, setLoading] = useState(false)
  const [activeConversation, setActiveConversation] = useState(null)

  const sendMessage = async () => {
    if (!inputText.trim()) return

    setLoading(true)

    // Add user message
    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: inputText,
    }
    setMessages((prev) => [...prev, userMessage])
    setInputText('')

    try {
      const response = await api.post('/chat/message', {
        tenant_key: 'demo',
        user_message: inputText,
        conversation_id: activeConversation,
      })

      // Add bot response
      setMessages((prev) =>
        prev.map((msg) =>
          msg.role === 'user' && msg.id === Date.now()
            ? { ...msg, reply: response.data.message }
            : msg,
        ),
      )
    } catch (err) {
      console.error('Chat error:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ minHeight: '100vh', display: 'flex' }}>
      {/* Sidebar */}
      <div style={{ width: '280px', background: '#1e1e2d', color: 'white', padding: '20px' }}>
        <h2 style={{ marginBottom: '30px' }}>SC Chatbot</h2>

        <button
          onClick={onLogout}
          style={{
            width: '100%',
            padding: '10px',
            background: '#d32f2f',
            border: 'none',
            borderRadius: '6px',
            color: 'white',
            cursor: 'pointer',
          }}
        >
          Logout
        </button>

        <div style={{ marginTop: '20px' }}>
          <h3 style={{ fontSize: '0.9rem' }}>Conversations</h3>
          <div style={{ marginTop: '10px' }}>
            <button
              onClick={() => setActiveConversation(null)}
              style={{
                width: '100%',
                padding: '8px',
                textAlign: 'left',
                background: 'rgba(255,255,255,0.1)',
                border: 'none',
                borderRadius: '4px',
                color: 'white',
                cursor: 'pointer',
              }}
            >
              New Chat
            </button>
          </div>
        </div>
      </div>

      {/* Chat area */}
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
          <div style={{ flex: 1, padding: '20px', overflow: 'auto' }}>
            {messages.length === 0 ? (
              <div style={{ textAlign: 'center', marginTop: '100px' }}>
                <h2>Welcome to SC Chatbot</h2>
                <p>Start a conversation with your AI assistant</p>
              </div>
            ) : (
              messages.map((msg) => (
                <div
                  key={msg.id}
                  style={{
                    marginBottom: '15px',
                    maxWidth: '80%',
                    background: msg.role === 'user' ? '#667eea' : '#fff',
                    color: 'white',
                    padding: '12px 16px',
                    borderRadius: '12px',
                    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
                  }}
                >
                  {msg.content}
                  {msg.reply && (
                    <div
                      style={{
                        marginTop: '8px',
                        padding: '8px 12px',
                        background: '#f1f1f1',
                        color: '#333',
                        borderRadius: '8px',
                        maxWidth: '80%',
                        alignSelf: 'flex-start',
                      }}
                    >
                      {msg.reply}
                    </div>
                  )}
                </div>
              ))
            )}
          </div>

          <div style={{ padding: '15px', background: '#f5f5f5', borderTop: '1px solid #eee' }}>
            <div style={{ display: 'flex', gap: '10px' }}>
              <input
                type="text"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                placeholder="Type a message..."
                style={{
                  flex: 1,
                  padding: '12px',
                  borderRadius: '8px',
                  border: '1px solid #ddd',
                }}
              />
              <button
                onClick={sendMessage}
                disabled={!inputText.trim() || loading}
                style={{
                  padding: '12px 20px',
                  background: '#667eea',
                  color: 'white',
                  border: 'none',
                  borderRadius: '8px',
                  cursor: loading ? 'not-allowed' : 'pointer',
                }}
              >
                Send
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}