import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import axios from 'axios'

import App from './App'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import ChatInterface from './pages/ChatInterface'
import Knowledge from './pages/Knowledge'
import Tools from './pages/Tools'
import './index.css'

// Configure axios defaults
axios.defaults.baseURL = '/api'
axios.defaults.headers.common['Content-Type'] = 'application/json'

// API client instance
const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const refreshToken = localStorage.getItem('refresh_token')
        if (refreshToken) {
          const response = await axios.post('/auth/refresh', { refresh_token: refreshToken })
          localStorage.setItem('access_token', response.data.access_token)
          localStorage.setItem('refresh_token', response.data.refresh_token)
          originalRequest.headers.Authorization = `Bearer ${response.data.access_token}`
          return api(originalRequest)
        }
      } catch (refreshError) {
        localStorage.clear()
        window.location.href = '/login'
        return { data: null }
      }
    }

    return Promise.reject(error)
  },
)

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<Login />} />
        <Route
          path="/dashboard"
          element={
            <Dashboard
              api={api}
              onLogout={() => {
                localStorage.clear()
                window.location.href = '/login'
              }}
            />
          }
        />
        <Route
          path="/chat"
          element={
            <ChatInterface
              api={api}
              onLogout={() => {
                localStorage.clear()
                window.location.href = '/login'
              }}
            />
          }
        />
        <Route
          path="/knowledge"
          element={
            <Knowledge
              api={api}
              onLogout={() => {
                localStorage.clear()
                window.location.href = '/login'
              }}
            />
          }
        />
        <Route
          path="/tools"
          element={
            <Tools
              api={api}
              onLogout={() => {
                localStorage.clear()
                window.location.href = '/login'
              }}
            />
          }
        />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>,
)