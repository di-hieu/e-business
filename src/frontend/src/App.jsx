import { Routes, Route } from 'react-router-dom'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import ChatInterface from './pages/ChatInterface'
import Knowledge from './pages/Knowledge'
import Analytics from './pages/Analytics'
import Settings from './pages/Settings'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Dashboard />} />
      <Route path="/login" element={<Login />} />
      <Route path="/chat" element={<ChatInterface />} />
      <Route path="/knowledge" element={<Knowledge />} />
      <Route path="/analytics" element={<Analytics />} />
      <Route path="/settings" element={<Settings />} />
    </Routes>
  )
}

export default App