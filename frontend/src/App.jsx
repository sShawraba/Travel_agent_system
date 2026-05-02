import React, { useState, useEffect } from 'react'
import './App.css'
import AuthPage from './pages/AuthPage'
import TravelPlannerPage from './pages/TravelPlannerPage'

function App() {
  const [token, setToken] = useState(null)
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  // Check if user has a valid token on app load
  useEffect(() => {
    const savedToken = localStorage.getItem('access_token')
    if (savedToken) {
      setToken(savedToken)
      // Verify token is still valid by calling /api/auth/me
      verifyToken(savedToken)
    } else {
      setLoading(false)
    }
  }, [])

  const verifyToken = async (tokenValue) => {
    try {
      const res = await fetch('http://localhost:8000/api/auth/me', {
        headers: {
          'Authorization': `Bearer ${tokenValue}`
        }
      })
      if (res.ok) {
        const userData = await res.json()
        setUser(userData)
      } else {
        // Token is invalid
        localStorage.removeItem('access_token')
        setToken(null)
      }
    } catch (err) {
      console.error('Token verification failed:', err)
      localStorage.removeItem('access_token')
      setToken(null)
    } finally {
      setLoading(false)
    }
  }

  const handleLogin = (newToken, userData) => {
    localStorage.setItem('access_token', newToken)
    setToken(newToken)
    setUser(userData)
  }

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    setToken(null)
    setUser(null)
  }

  if (loading) {
    return <div className="loading">Loading...</div>
  }

  if (!token) {
    return <AuthPage onLogin={handleLogin} />
  }

  return <TravelPlannerPage user={user} onLogout={handleLogout} token={token} />
}

export default App


export default App
