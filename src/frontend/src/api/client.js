import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor for adding auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor for handling token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      const refresh_token = localStorage.getItem('refresh_token')
      if (refresh_token) {
        try {
          const response = await axios.post(`${API_URL}/auth/refresh`, {
            refresh_token,
          })
          const { access_token } = response.data
          localStorage.setItem('access_token', access_token)

          originalRequest.headers.Authorization = `Bearer ${access_token}`
          return api(originalRequest)
        } catch (refreshError) {
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          window.location.href = '/login'
        }
      }
    }

    return Promise.reject(error)
  }
)

// Auth API
export const authAPI = {
  login: (data) => api.post('/auth/login', data),
  register: (data) => api.post('/auth/register', data),
  logout: () => api.post('/auth/logout'),
  getCurrentUser: () => api.get('/auth/me'),
  refresh: (refreshToken) => api.post('/auth/refresh', { refresh_token: refreshToken }),
}

// Chat API
export const chatAPI = {
  sendMessage: (data) => api.post('/chat/message', data),
  getConversations: (userId) => api.get('/chat/conversations', { params: { userId } }),
  getConversation: (conversationId) => api.get(`/chat/conversations/${conversationId}`),
}

// Knowledge API
export const knowledgeAPI = {
  upload: (file, tenantKey, apiKey) => {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('tenant_key', tenantKey)
    formData.append('api_key', apiKey)
    return api.post('/knowledge/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
  list: (tenantKey, apiKey) =>
    api.get('/knowledge/list', {
      params: { tenant_key: tenantKey, api_key: apiKey },
    }),
  delete: (docId, tenantKey, apiKey) =>
    api.delete(`/knowledge/${docId}`, {
      params: { tenant_key: tenantKey, api_key: apiKey },
    }),
  toggle: (docId, is_active, tenantKey, apiKey) =>
    api.put(`/knowledge/${docId}/active`, { is_active, tenant_key: tenantKey, api_key: apiKey }),
}

// Tools API
export const toolsAPI = {
  list: (tenantKey, apiKey) =>
    api.get('/tools/definitions', {
      params: { tenant_key: tenantKey, api_key: apiKey },
    }),
  execute: (toolName, params, tenantKey, apiKey) =>
    api.post('/tools/execute', { tool_name: toolName, parameters: params }, {
      params: { tenant_key: tenantKey, api_key: apiKey },
    }),
  define: (toolData) => api.post('/tools/define', toolData),
  delete: (toolId, tenantKey, apiKey) =>
    api.delete(`/tools/${toolId}`, {
      params: { tenant_key: tenantKey, api_key: apiKey },
    }),
}

// Admin API
export const adminAPI = {
  analytics: (tenantKey, apiKey) =>
    api.get('/admin/analytics', {
      params: { tenant_key: tenantKey, api_key: apiKey },
    }),
  users: (tenantKey, apiKey) =>
    api.get('/admin/users', {
      params: { tenant_key: tenantKey, api_key: apiKey },
    }),
  documents: (tenantKey, apiKey) =>
    api.get('/admin/documents', {
      params: { tenant_key: tenantKey, api_key: apiKey },
    }),
  tools: (tenantKey, apiKey) =>
    api.get('/admin/tools', {
      params: { tenant_key: tenantKey, api_key: apiKey },
    }),
  conversations: (tenantKey, apiKey) =>
    api.get('/admin/conversations', {
      params: { tenant_key: tenantKey, api_key: apiKey },
    }),
  settings: (tenantKey, apiKey) =>
    api.get('/admin/settings', {
      params: { tenant_key: tenantKey, api_key: apiKey },
    }),
  updateSettings: (data, tenantKey, apiKey) =>
    api.post('/admin/settings', data, {
      params: { tenant_key: tenantKey, api_key: apiKey },
    }),
}

// Webhooks API (for testing)
export const webhookAPI = {
  testZalo: (payload) => api.post('/webhooks/zalo', payload),
  testFacebook: (payload) => api.post('/webhooks/facebook', payload),
  testInstagram: (payload) => api.post('/webhooks/instagram', payload),
}

export default api