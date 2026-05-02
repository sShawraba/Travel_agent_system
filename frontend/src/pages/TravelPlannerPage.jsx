import React, { useState, useEffect } from 'react'
import '../styles/TravelPlanner.css'

function TravelPlannerPage({ user, onLogout, token }) {
  const [query, setQuery] = useState('')
  const [response, setResponse] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [history, setHistory] = useState([])
  const [showHistory, setShowHistory] = useState(false)

  // Load agent run history on mount
  useEffect(() => {
    loadHistory()
  }, [])

  const loadHistory = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/agent-runs', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      
      if (res.ok) {
        const data = await res.json()
        setHistory(data)
      }
    } catch (err) {
      console.error('Failed to load history:', err)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResponse(null)

    try {
      const res = await fetch('http://localhost:8000/api/plan-trip', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ query }),
      })

      if (!res.ok) {
        const errorData = await res.json()
        throw new Error(errorData.detail || `API error: ${res.status}`)
      }

      const data = await res.json()
      setResponse(data)
      setQuery('')
      
      // Refresh history
      loadHistory()
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleLoadRun = (run) => {
    setResponse({
      recommended_destination: run.recommended_destination,
      travel_style: run.travel_style,
      explanation: run.explanation,
      weather_summary: run.weather_summary
    })
    setShowHistory(false)
  }

  return (
    <div className="container">
      <header className="header">
        <div className="header-content">
          <div>
            <h1>✈️ Smart Travel Planner</h1>
            <p>AI-powered travel planning</p>
          </div>
          <div className="user-info">
            <span>👤 {user?.username || user?.email}</span>
            <div className="header-buttons">
              <button 
                onClick={() => setShowHistory(!showHistory)}
                className="button-secondary"
              >
                📋 History ({history.length})
              </button>
              <button 
                onClick={onLogout}
                className="button-secondary logout"
              >
                🚪 Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      {showHistory && (
        <div className="history-panel">
          <h3>Your Trip Plans</h3>
          {history.length === 0 ? (
            <p className="empty">No trips planned yet</p>
          ) : (
            <div className="history-list">
              {history.map((run) => (
                <div 
                  key={run.id} 
                  className="history-item"
                  onClick={() => handleLoadRun(run)}
                >
                  <div className="history-destination">
                    📍 {run.recommended_destination || 'Pending'}
                  </div>
                  <div className="history-query">{run.query.substring(0, 50)}...</div>
                  <div className="history-date">
                    {new Date(run.created_at).toLocaleDateString()}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      <main className="main">
        <form onSubmit={handleSubmit} className="form">
          <textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Describe your ideal trip (e.g., 'I want to relax at a beach in Southeast Asia with good food')"
            className="input textarea"
            disabled={loading}
            rows={3}
          />
          <button type="submit" className="button" disabled={loading || !query.trim()}>
            {loading ? 'Planning...' : '✨ Plan My Trip'}
          </button>
        </form>

        {error && (
          <div className="error">
            <p>❌ Error: {error}</p>
          </div>
        )}

        {response && (
          <div className="response">
            <h2>🎯 Your Travel Plan</h2>
            
            <div className="result-card destination">
              <h3>📍 Destination</h3>
              <p className="highlight">{response.recommended_destination}</p>
            </div>

            <div className="result-card style">
              <h3>🎨 Travel Style</h3>
              <p className="highlight">{response.travel_style.charAt(0).toUpperCase() + response.travel_style.slice(1)}</p>
            </div>

            <div className="result-card explanation">
              <h3>💡 Why This Destination</h3>
              <p>{response.explanation}</p>
            </div>

            <div className="result-card weather">
              <h3>🌤️ Current Weather</h3>
              <p>{response.weather_summary}</p>
            </div>
          </div>
        )}

        {!response && !error && !loading && (
          <div className="empty-state">
            <p>🌍 Start by describing your ideal trip!</p>
            <p className="hint">Tell us about your preferences, budget, and travel style</p>
          </div>
        )}
      </main>
    </div>
  )
}

export default TravelPlannerPage
