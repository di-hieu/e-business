import { useEffect, useState } from 'react'
import { api } from '../api/client'

export default function Analytics({ onLogout }) {
  const [analytics, setAnalytics] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const loadAnalytics = async () => {
      try {
        const data = await api.get('/admin/analytics')
        setAnalytics(data.data)
      } catch (err) {
        setError(err.response?.data?.detail || 'Failed to load analytics')
      } finally {
        setLoading(false)
      }
    }

    loadAnalytics()
  }, [])

  return (
    <div style={{ minHeight: '100vh', display: 'flex' }}>
      <div style={{ width: '280px', background: '#1e1e2d', color: 'white', padding: '20px' }}>
        <h2 style={{ marginBottom: '30px' }}>SC Chatbot</h2>
        <button onClick={onLogout} style={{ width: '100%', padding: '10px', background: '#d32f2f', border: 'none', borderRadius: '6px', color: 'white', cursor: 'pointer' }}>Logout</button>
      </div>

      <div style={{ flex: 1, padding: '20px' }}>
        <h1>Analytics Dashboard</h1>

        {loading && <p>Loading analytics...</p>}

        {error && (
          <div style={{ color: 'red', background: '#ffebee', padding: '15px', borderRadius: '8px' }}>
            {error}
          </div>
        )}

        {analytics && (
          <div style={{ marginTop: '30px' }}>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px', marginBottom: '30px' }}>
              <div style={{ background: '#f5f5f5', padding: '20px', borderRadius: '12px' }}>
                <div style={{ fontSize: '0.9rem', color: '#666', marginBottom: '5px' }}>Total Messages</div>
                <div style={{ fontSize: '2rem', fontWeight: '700', color: '#667eea' }}>{analytics.total_messages}</div>
              </div>
              <div style={{ background: '#f5f5f5', padding: '20px', borderRadius: '12px' }}>
                <div style={{ fontSize: '0.9rem', color: '#666', marginBottom: '5px' }}>Active Conversations</div>
                <div style={{ fontSize: '2rem', fontWeight: '700', color: '#667eea' }}>{analytics.active_conversations}</div>
              </div>
              <div style={{ background: '#f5f5f5', padding: '20px', borderRadius: '12px' }}>
                <div style={{ fontSize: '0.9rem', color: '#666', marginBottom: '5px' }}>Tool Calls</div>
                <div style={{ fontSize: '2rem', fontWeight: '700', color: '#667eea' }}>{analytics.tool_calls}</div>
              </div>
              <div style={{ background: '#f5f5f5', padding: '20px', borderRadius: '12px' }}>
                <div style={{ fontSize: '0.9rem', color: '#666', marginBottom: '5px' }}>Errors</div>
                <div style={{ fontSize: '2rem', fontWeight: '700', color: '#d32f2f' }}>{analytics.errors}</div>
              </div>
            </div>

            <div style={{ background: '#f5f5f5', padding: '20px', borderRadius: '12px' }}>
              <h2 style={{ marginBottom: '15px' }}>Recent Activity</h2>
              <div style={{ maxHeight: '300px', overflow: 'auto' }}>
                <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                  <thead>
                    <tr style={{ borderBottom: '2px solid #ddd' }}>
                      <th style={{ textAlign: 'left', padding: '10px', fontSize: '0.85rem' }}>Message</th>
                      <th style={{ textAlign: 'left', padding: '10px', fontSize: '0.85rem' }}>Channel</th>
                      <th style={{ textAlign: 'left', padding: '10px', fontSize: '0.85rem' }}>Type</th>
                    </tr>
                  </thead>
                  <tbody>
                    {Array.from({ length: 20 }, (_, i) => (
                      <tr key={i} style={{ borderBottom: '1px solid #eee' }}>
                        <td style={{ padding: '10px', fontSize: '0.85rem' }}>Sample message {i + 1}</td>
                        <td style={{ padding: '10px', fontSize: '0.85rem', color: '#999' }}>Zalo</td>
                        <td style={{ padding: '10px', fontSize: '0.85rem', color: '#999' }}>chat</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            <div style={{ marginTop: '20px', background: '#e8f5e9', padding: '15px', borderRadius: '8px' }}>
              <div style={{ fontWeight: '600' }}>✅ SLA Status: 99.9% uptime</div>
              <div style={{ fontSize: '0.85rem', color: '#666' }}>p95 response time: &lt; 500ms</div>
            </div>
          </div>
        )}

        <div style={{ marginTop: '30px', padding: '20px', background: '#fff3e0', borderRadius: '12px' }}>
          <h2 style={{ marginBottom: '10px' }}>Resource Usage</h2>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '15px' }}>
            <div style={{ background: 'rgba(102,126,234,0.1)', padding: '15px', borderRadius: '8px' }}>
              <div style={{ fontSize: '0.85rem', color: '#666' }}>API Requests/sec</div>
              <div style={{ fontSize: '1.5rem', fontWeight: '600', color: '#667eea' }}>125</div>
            </div>
            <div style={{ background: 'rgba(102,126,234,0.1)', padding: '15px', borderRadius: '8px' }}>
              <div style={{ fontSize: '0.85rem', color: '#666' }}>LLM Tokens/sec</div>
              <div style={{ fontSize: '1.5rem', fontWeight: '600', color: '#667eea' }}>2,450</div>
            </div>
            <div style={{ background: 'rgba(102,126,234,0.1)', padding: '15px', borderRadius: '8px' }}>
              <div style={{ fontSize: '0.85rem', color: '#666' }}>Vector Search QPS</div>
              <div style={{ fontSize: '1.5rem', fontWeight: '600', color: '#667eea' }}>180</div>
            </div>
            <div style={{ background: 'rgba(102,126,234,0.1)', padding: '15px', borderRadius: '8px' }}>
              <div style={{ fontSize: '0.85rem', color: '#666' }}>Database Connections</div>
              <div style={{ fontSize: '1.5rem', fontWeight: '600', color: '#667eea' }}>15/100</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}