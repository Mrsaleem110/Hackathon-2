import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './App.css'
import FrontendEnvValidator from './utils/envValidator.js'

// Validate environment variables before starting the app
FrontendEnvValidator.validateAndLog()

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)