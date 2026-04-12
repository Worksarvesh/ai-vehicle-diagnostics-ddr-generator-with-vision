import { useState } from 'react'

const API_BASE = import.meta.env.DEV ? 'http://localhost:8000' : '/api'

export default function App() {
  const [formData, setFormData] = useState({
    engine_temp: '',
    brake_wear_pct: '',
    battery_voltage: '',
    tire_pressure: '',
    chain_tension: '',
    ambient_temp: '',
    smoke_detected: false,
    abnormal_noise: false,
    api_key: 'demo-key',
  })

  const [image, setImage] = useState(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
  }

  const handleImageChange = (e) => {
    setImage(e.target.files[0])
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const payload = new FormData()
      payload.append('engine_temp', formData.engine_temp)
      payload.append('brake_wear_pct', formData.brake_wear_pct)
      payload.append('battery_voltage', formData.battery_voltage)
      payload.append('tire_pressure', formData.tire_pressure)
      payload.append('chain_tension', formData.chain_tension)
      payload.append('ambient_temp', formData.ambient_temp)
      payload.append('smoke_detected', formData.smoke_detected)
      payload.append('abnormal_noise', formData.abnormal_noise)

      if (image) {
        payload.append('image', image)
      }

      const response = await fetch(`${API_BASE}/predict-image`, {
        method: 'POST',
        headers: {
          'X-API-KEY': formData.api_key,
        },
        body: payload,
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Prediction failed')
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-shell">
      <header>
        <h1>AI Vehicle Diagnostics</h1>
        <p>Fast vehicle inspection predictions with confidence and recommendation clarity.</p>
      </header>

      <main>
        <form onSubmit={handleSubmit} className="panel">
          <div className="form-row">
            <label htmlFor="engine_temp">Engine Temp (°C)</label>
            <input
              id="engine_temp"
              name="engine_temp"
              type="number"
              min="0"
              max="250"
              step="0.1"
              value={formData.engine_temp}
              onChange={handleInputChange}
              required
            />
          </div>

          <div className="form-row">
            <label htmlFor="brake_wear_pct">Brake Wear (%)</label>
            <input
              id="brake_wear_pct"
              name="brake_wear_pct"
              type="number"
              min="0"
              max="100"
              step="0.1"
              value={formData.brake_wear_pct}
              onChange={handleInputChange}
              required
            />
          </div>

          <div className="form-row">
            <label htmlFor="battery_voltage">Battery Voltage</label>
            <input
              id="battery_voltage"
              name="battery_voltage"
              type="number"
              min="0"
              max="30"
              step="0.1"
              value={formData.battery_voltage}
              onChange={handleInputChange}
              required
            />
          </div>

          <div className="form-row">
            <label htmlFor="tire_pressure">Tire Pressure (PSI)</label>
            <input
              id="tire_pressure"
              name="tire_pressure"
              type="number"
              min="0"
              max="60"
              step="0.1"
              value={formData.tire_pressure}
              onChange={handleInputChange}
              required
            />
          </div>

          <div className="form-row">
            <label htmlFor="chain_tension">Chain Tension</label>
            <input
              id="chain_tension"
              name="chain_tension"
              type="number"
              min="0"
              max="100"
              step="0.1"
              value={formData.chain_tension}
              onChange={handleInputChange}
              required
            />
          </div>

          <div className="form-row">
            <label htmlFor="ambient_temp">Ambient Temp (°C)</label>
            <input
              id="ambient_temp"
              name="ambient_temp"
              type="number"
              min="-40"
              max="80"
              step="0.1"
              value={formData.ambient_temp}
              onChange={handleInputChange}
              required
            />
          </div>

          <div className="form-row toggle-row">
            <label>
              <input
                name="smoke_detected"
                type="checkbox"
                checked={formData.smoke_detected}
                onChange={handleInputChange}
              />
              Smoke detected
            </label>
            <label>
              <input
                name="abnormal_noise"
                type="checkbox"
                checked={formData.abnormal_noise}
                onChange={handleInputChange}
              />
              Abnormal noise
            </label>
          </div>

          <div className="form-row">
            <label htmlFor="inspection_image">Inspection Image</label>
            <input
              id="inspection_image"
              type="file"
              accept="image/*"
              onChange={handleImageChange}
            />
            <p className="hint">Optional: upload a diagnostic image to improve prediction.</p>
          </div>

          <div className="form-row">
            <label htmlFor="api_key">API Key</label>
            <input
              id="api_key"
              type="password"
              placeholder="demo-key"
              value={formData.api_key}
              onChange={(e) => setFormData(prev => ({ ...prev, api_key: e.target.value }))}
              required
            />
          </div>

          <button type="submit" className="primary-button" disabled={loading}>
            {loading ? 'Predicting...' : 'Predict'}
          </button>
        </form>

        {loading && (
          <section className="panel">
            <div className="status-box loading">Predicting vehicle diagnostics...</div>
          </section>
        )}

        {error && (
          <section className="panel">
            <div className="status-box error">
              <strong>Error:</strong> {error}
            </div>
          </section>
        )}

        {result && (
          <section className="panel">
            <div className="status-box success">Prediction complete</div>
            <div className="result-card">
              <h2>Severity: <span className={`severity-${result.predicted_severity}`}>{result.predicted_severity}</span></h2>
              <p><strong>Confidence:</strong> {Math.round(result.confidence * 100)}%</p>
              <h3>Probability Distribution</h3>
              <ul>
                {Object.entries(result.probabilities).map(([level, score]) => (
                  <li key={level}>{level}: {Math.round(score * 100)}%</li>
                ))}
              </ul>
              {result.image_features && (
                <>
                  <h3>Image Feature Summary</h3>
                  <ul>
                    {Object.entries(result.image_features).map(([name, value]) => (
                      <li key={name}><strong>{name}:</strong> {value}</li>
                    ))}
                  </ul>
                </>
              )}
              <p className="note">{result.message}</p>
            </div>
          </section>
        )}
      </main>
    </div>
  )
}
