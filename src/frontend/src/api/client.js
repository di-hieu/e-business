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
  sendMessage: (data) => api.post('/api/chat/message', data),
  getConversations: (userId) => api.get('/api/chat/conversations', { params: { userId } }),
  getConversation: (conversationId) => api.get(`/api/chat/conversations/${conversationId}`),
}

// Knowledge API
export const knowledgeAPI = {
  upload: (file, tenantKey, apiKey) => {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('tenant_key', tenantKey)
    formData.append('api_key', apiKey)
    return api.post('/api/knowledge/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
  list: (tenantKey, apiKey) =>
    api.get('/api/knowledge/list', {
      params: { tenant_key: tenantKey, api_key: apiKey },
    }),
  delete: (docId, tenantKey, apiKey) =>
    api.delete(`/api/knowledge/${docId}`, {
      params: { tenant_key: tenantKey, api_key: apiKey },
    }),
  toggle: (docId, is_active, tenantKey, apiKey) =>
    api.put(`/api/knowledge/${docId}/active`, { is_active, tenant_key: tenantKey, api_key: apiKey }),
}

// Tools API
export const toolsAPI = {
  list: (tenantKey, apiKey) =>
    api.get('/api/tools', {
      params: { tenant_key: tenantKey, api_key: apiKey },
    }),
  execute: (toolName, params, tenantKey, apiKey) =>
    api.post('/api/tools/register', { tool_name: toolName, parameters: params }, {
      params: { tenant_key: tenantKey, api_key: apiKey },
    }),
  define: (toolData) => api.post('/api/tools/register', toolData),
  delete: (toolId, tenantKey, apiKey) =>
    api.delete(`/api/tools/${toolId}`, {
      params: { tenant_key: tenantKey, api_key: apiKey },
    }),
}

// Admin API
export const adminAPI = {
  analytics: (tenantKey, apiKey) =>
    api.get('/api/admin/analytics', {
      params: { tenant_key: tenantKey, api_key: apiKey },
    }),
  users: (tenantKey, apiKey) =>
    api.get('/api/admin/users', {
      params: { tenant_key: tenantKey, api_key: apiKey },
    }),
  tenants: (tenantKey, apiKey) =>
    api.get('/api/admin/tenants', {
      params: { tenant_key: tenantKey, api_key: apiKey },
    }),
  documents: (tenantKey, apiKey) =>
    api.get('/api/admin/documents', {
      params: { tenant_key: tenantKey, api_key: apiKey },
    }),
  tools: (tenantKey, apiKey) =>
    api.get('/api/admin/tools', {
      params: { tenant_key: tenantKey, api_key: apiKey },
    }),
  conversations: (tenantKey, apiKey) =>
    api.get('/api/admin/conversations', {
      params: { tenant_key: tenantKey, api_key: apiKey },
    }),
  settings: (tenantKey, apiKey) =>
    api.get('/api/admin/settings', {
      params: { tenant_key: tenantKey, api_key: apiKey },
    }),
  updateSettings: (data, tenantKey, apiKey) =>
    api.post('/api/admin/settings', data, {
      params: { tenant_key: tenantKey, api_key: apiKey },
    }),
  configVariables: (tenantKey, apiKey) =>
    api.get('/api/config/variables', {
      params: { tenant_key: tenantKey, api_key: apiKey },
    }),
  updateConfigVariables: (data, tenantKey, apiKey) =>
    api.post('/api/config/variables', data, {
      params: { tenant_key: tenantKey, api_key: apiKey },
    }),
  configDefaults: (tenantKey, apiKey) =>
    api.get('/api/config/defaults', {
      params: { tenant_key: tenantKey, api_key: apiKey },
    }),
  configStatus: (tenantKey, apiKey) =>
    api.get('/api/config/status', {
      params: { tenant_key: tenantKey, api_key: apiKey },
    }),
}

// Webhooks API (for testing)
export const webhookAPI = {
  testZalo: (payload) => api.post('/api/webhooks/zalo', payload),
  testFacebook: (payload) => api.post('/api/webhooks/facebook', payload),
  testInstagram: (payload) => api.post('/api/webhooks/instagram', payload),
}

export { api }
export default api