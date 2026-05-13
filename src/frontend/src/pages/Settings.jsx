import { useState, useEffect } from 'react'
import { api } from '../api/client'

export default function Settings({ onLogout }) {
  const [loading, setLoading] = useState(false)
  const [submitting, setSubmitting] = useState(false)
  const [categories, setCategories] = useState([])
  const [variables, setVariables] = useState({})

  // Load configuration categories and variables
  const loadConfig = async () => {
    try {
      // First get categories
      const catData = await api.get('/config/categories')
      const categoriesList = catData.data
      
      // Then get all variables
      const varData = await api.get('/config/variables')
      const allVariables = varData.data
      
      // Group variables by category
      const grouped = {}
      for (const v of allVariables) {
        if (!grouped[v.category]) {
          grouped[v.category] = []
        }
        grouped[v.category].push(v)
      }
      
      setCategories(categoriesList)
      setVariables(grouped)
    } catch (err) {
      console.error('Failed to load config:', err)
    }
  }

  const handleUpdateConfig = async (key, value) => {
    setVariables(prev => ({
      ...prev,
      [key]: { ...prev[key], current_value: value }
    }))
    
    try {
      await api.post(`/config/variables/${key}`, { value })
      // Success - refresh config to show updated values
      const varData = await api.get('/config/variables')
      setVariables(varData.data)
    } catch (err) {
      console.error('Failed to save config:', err)
    }
  }

  useEffect(() => {
    loadConfig()
  }, [])

  // Generate description text
  const getDescription = (key) => {
    const descMap = {
      'LLM_API_KEY': 'OpenAI API key or OpenRouter API key for LLM access',
      'LLM_MODEL': 'LLM model to use (gpt-4o-mini, gpt-4o, claude-3-5-sonnet, etc.)',
      'EMBEDDING_MODEL': 'Embedding model for vector search (e.g., all-MiniLM-L6-v2)',
      'TELEGRAM_BOT_TOKEN': 'Telegram Bot token from @BotFather',
      'TELEGRAM_WEBHOOK_URL': 'Telegram webhook URL (https://your-domain.com/webhooks/telegram)',
      'ZALO_APP_ID': 'Zalo Official Account App ID',
      'ZALO_APP_SECRET': 'Zalo Official Account App Secret',
      'FACEBOOK_APP_ID': 'Facebook Messenger App ID',
      'FACEBOOK_APP_SECRET': 'Facebook Messenger App Secret',
      'OPENROUTER_API_KEY': 'OpenRouter API key for multi-model support',
    }
    return descMap[key] || 'Configuration option'
  }

  return (
    <div style={{ minHeight: '100vh', display: 'flex' }}>
      <div style={{ width: '280px', background: '#1e1e2d', color: 'white', padding: '20px' }}>
        <h2 style={{ marginBottom: '30px' }}>SC Chatbot</h2>
        <button onClick={onLogout} style={{ width: '100%', padding: '10px', background: '#d32f2f', border: 'none', borderRadius: '6px', color: 'white', cursor: 'pointer' }}>Logout</button>
      </div>

      <div style={{ flex: 1, padding: '20px' }}>
        <h1>Environment Configuration</h1>
        <p style={{ color: '#666', marginBottom: '20px' }}>
          Configure your application settings. Sensitive values (API keys) are hidden.
        </p>

        {categories.map(cat => (
          <div key={cat} style={{ marginTop: '30px', padding: '15px', background: '#f8f9fa', borderRadius: '8px' }}>
            <h2 style={{ margin: '0 0 15px 0', color: '#667eea' }}>{cat}</h2>
            
            {(variables[cat] || []).map(v => (
              <div key={v.key} style={{ marginBottom: '15px' }}>
                <label style={{ display: 'block', marginBottom: '5px', fontWeight: '600', fontSize: '0.9rem' }}>
                  {v.key}
                  {v.required && <span style={{ color: '#d32f2f', marginLeft: '5px' }}>*</span>}
                </label>
                <div style={{ fontSize: '0.8rem', color: '#666', marginBottom: '8px' }}>
                  {getDescription(v.key)}
                </div>
                <input
                  type={v.key.includes('_KEY') || v.key.includes('SECRET') || v.key.includes('TOKEN') ? 'password' : 'text'}
                  value={v.current_value || ''}
                  onChange={(e) => handleUpdateConfig(v.key, e.target.value)}
                  style={{ 
                    width: '100%', 
                    padding: '10px', 
                    borderRadius: '6px', 
                    border: '1px solid #ddd',
                    fontSize: '0.9rem',
                  }}
                  placeholder={`Enter ${v.key}...`}
                />
                {v.sensitive && (
                  <span style={{ 
                    display: 'block', 
                    fontSize: '0.7rem', 
                    color: '#d32f2f', 
                    marginTop: '5px'
                  }}>
                    ⚠️ Sensitive - Keep secure
                  </span>
                )}
              </div>
            ))}
          </div>
        ))}

        <div style={{ marginTop: '30px', display: 'flex', gap: '10px' }}>
          <button
            onClick={() => { loadConfig(); }}
            disabled={loading}
            style={{
              padding: '12px 24px',
              background: '#6c757d',
              color: 'white',
              border: 'none',
              borderRadius: '6px',
              cursor: loading ? 'not-allowed' : 'pointer',
            }}
          >
            Refresh
          </button>
        </div>
      </div>
    </div>
  )
}