import { useEffect, useState } from 'react'
import { api } from '../api/client'

export default function Dashboard({ onLogout }) {
  const [conversations, setConversations] = useState([])
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('conversations')

  const loadConversations = async () => {
    try {
      const data = await api.get('/conversations')
      setConversations(data.data)
    } catch (err) {
      console.error('Failed to load conversations:', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadConversations()
  }, [])

  return (
    <div style={{ minHeight: '100vh', display: 'flex' }}>
      {/* Sidebar */}
      <div style={{ width: '250px', background: '#1e1e2d', color: 'white', padding: '20px' }}>
        <h2 style={{ marginBottom: '30px' }}>SC Chatbot</h2>
        
        <nav>
          <button
            onClick={() => setActiveTab('conversations')}
            style={{
              width: '100%',
              padding: '10px',
              textAlign: 'left',
              background: 'none',
              border: 'none',
              color: 'white',
              cursor: 'pointer',
              borderBottom: '1px solid rgba(255,255,255,0.1)',
            }}
          >
            💬 Conversations
          </button>
          <button
            onClick={() => setActiveTab('knowledge')}
            style={{
              width: '100%',
              padding: '10px',
              textAlign: 'left',
              background: 'none',
              border: 'none',
              color: 'white',
              cursor: 'pointer',
              borderBottom: '1px solid rgba(255,255,255,0.1)',
            }}
          >
            📚 Knowledge
          </button>
          <button
            onClick={() => setActiveTab('tools')}
            style={{
              width: '100%',
              padding: '10px',
              textAlign: 'left',
              background: 'none',
              border: 'none',
              color: 'white',
              cursor: 'pointer',
              borderBottom: '1px solid rgba(255,255,255,0.1)',
            }}
          >
            🔧 Tools
          </button>
        </nav>

        <button
          onClick={onLogout}
          style={{
            width: '100%',
            padding: '10px',
            marginTop: '30px',
            background: '#d32f2f',
            border: 'none',
            borderRadius: '6px',
            color: 'white',
            cursor: 'pointer',
          }}
        >
          Logout
        </button>
      </div>

      {/* Main content */}
      <div style={{ flex: 1, padding: '20px' }}>
        <div style={{ maxWidth: '800px' }}>
          <h1>Dashboard</h1>

          {activeTab === 'conversations' && (
            <div>
              {loading ? (
                <p>Loading conversations...</p>
              ) : (
                <div style={{ display: 'grid', gap: '10px' }}>
                  {conversations.length === 0 ? (
                    <p>No conversations yet.</p>
                  ) : (
                    conversations.map((conv) => (
                      <div
                        key={conv.id}
                        onClick={() => {}}
                        style={{
                          padding: '15px',
                          background: '#fff',
                          borderRadius: '8px',
                          boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
                          cursor: 'pointer',
                        }}
                      >
                        <div style={{ fontWeight: '600' }}>{conv.title || 'New conversation'}</div>
                        <div style={{ fontSize: '0.85rem', color: '#666' }}>
                          {conv.channel || 'General'} · {new Date(conv.created_at).toLocaleString()}
                        </div>
                      </div>
                    ))
                  )}
                </div>
              )}
            </div>
          )}

          {activeTab === 'knowledge' && (
            <div>
              <h2>Knowledge Base</h2>
              <p>Upload PDF, text files to build your knowledge base.</p>
              <button style={{ padding: '10px 20px', background: '#667eea', color: 'white', border: 'none', borderRadius: '6px', cursor: 'pointer' }}>
                Upload Files
              </button>
            </div>
          )}

          {activeTab === 'tools' && (
            <div>
              <h2>Tools</h2>
              <p>Configure custom tools for your chatbot.</p>
              <button style={{ padding: '10px 20px', background: '#667eea', color: 'white', border: 'none', borderRadius: '6px', cursor: 'pointer' }}>
                Add Tool
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}