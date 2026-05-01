import React, { useState } from 'react'
import './App.css'

function App() {
  const [query, setQuery] = useState('')
  const [response, setResponse] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

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
        },
        body: JSON.stringify({ query }),
      })

      if (!res.ok) {
        throw new Error(`API error: ${res.status}`)
      }

      const data = await res.json()
      setResponse(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <header className="header">
        <h1>✈️ Smart Travel Planner</h1>
        <p>AI-powered travel planning</p>
      </header>

      <main className="main">
        <form onSubmit={handleSubmit} className="form">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Describe your ideal trip (e.g., 'I want to relax at a beach')"
            className="input"
            disabled={loading}
          />
          <button type="submit" className="button" disabled={loading}>
            {loading ? 'Planning...' : 'Plan My Trip'}
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
            
            <div className="result-card">
              <h3>📍 Destination</h3>
              <p className="highlight">{response.recommended_destination}</p>
            </div>

            <div className="result-card">
              <h3>🎨 Travel Style</h3>
              <p className="highlight">{response.travel_style.charAt(0).toUpperCase() + response.travel_style.slice(1)}</p>
            </div>

            <div className="result-card">
              <h3>💡 Why This Destination</h3>
              <p>{response.explanation}</p>
            </div>

            <div className="result-card">
              <h3>🌤️ Current Weather</h3>
              <p>{response.weather_summary}</p>
            </div>
          </div>
        )}

        {!response && !error && !loading && (
          <div className="empty-state">
            <p>Start by describing your ideal trip!</p>
          </div>
        )}
      </main>
    </div>
  )
}

export default App
