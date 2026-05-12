import { useState } from 'react'
import { api } from '../api/client'

export default function Knowledge({ onLogout }) {
  const [documents, setDocuments] = useState([])
  const [loading, setLoading] = useState(false)
  const [draggedFile, setDraggedFile] = useState(null)

  const uploadFile = async (file) => {
    setLoading(true)

    const formData = new FormData()
    formData.append('file', file)
    formData.append('tenant_key', 'demo')
    formData.append('api_key', 'demo-api-key')
    formData.append('is_active', true)

    try {
      await api.post('/knowledge/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      setDocuments((prev) => [...prev, { id: Date.now(), name: file.name, uploaded: true }])
    } catch (err) {
      console.error('Upload error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleDragOver = (e) => {
    e.preventDefault()
  }

  const handleDrop = (e) => {
    e.preventDefault()
    const file = e.dataTransfer.files[0]
    if (file) {
      setDraggedFile(file)
      uploadFile(file)
    }
  }

  return (
    <div style={{ minHeight: '100vh', display: 'flex' }}>
      <div style={{ width: '280px', background: '#1e1e2d', color: 'white', padding: '20px' }}>
        <h2 style={{ marginBottom: '30px' }}>SC Chatbot</h2>
        <button onClick={onLogout} style={{ width: '100%', padding: '10px', background: '#d32f2f', border: 'none', borderRadius: '6px', color: 'white', cursor: 'pointer' }}>Logout</button>
      </div>

      <div style={{ flex: 1, padding: '20px' }}>
        <h1>Knowledge Base</h1>
        <p>Upload PDF, text files to build your knowledge base for RAG</p>

        <div
          style={{
            border: '2px dashed #ccc',
            borderRadius: '12px',
            padding: '40px',
            textAlign: 'center',
            marginTop: '20px',
            background: '#fafafa',
          }}
          onDragOver={handleDragOver}
          onDrop={handleDrop}
        >
          {draggedFile ? (
            <p>Uploading: {draggedFile.name}...</p>
          ) : (
            <>
              <p style={{ fontSize: '1.2rem', color: '#666' }}>Drag & drop files here</p>
              <p style={{ color: '#999' }}>or</p>
              <label style={{ display: 'inline-block', padding: '12px 24px', background: '#667eea', color: 'white', borderRadius: '8px', cursor: 'pointer', marginTop: '10px' }}>
                Choose Files
                <input type="file" onChange={(e) => e.target.files[0] && uploadFile(e.target.files[0])} style={{ display: 'none' }} />
              </label>
              <p style={{ color: '#666', fontSize: '0.9rem' }}>Support: PDF, TXT, DOC (max 10MB)</p>
            </>
          )}
        </div>

        <div style={{ marginTop: '30px' }}>
          <h2>Uploaded Documents</h2>
          <div style={{ display: 'grid', gap: '10px' }}>
            {documents.length === 0 ? (
              <p style={{ color: '#999' }}>No documents uploaded yet</p>
            ) : (
              documents.map((doc) => (
                <div key={doc.id} style={{ padding: '12px', background: '#fff', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <span style={{ fontWeight: '500' }}>{doc.name}</span>
                    <span style={{ color: '#999', fontSize: '0.85rem' }}>{doc.uploaded ? '✓ Uploaded' : 'Uploading...'}</span>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  )
}