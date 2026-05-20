import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

import keycloak from './keycloak'

keycloak
  .init({
    onLoad: 'login-required',
    pkceMethod: 'S256',
  })
  .then((authenticated) => {
    if (!authenticated) {
      console.log('Not authenticated')
      return
    }

    setInterval(() => {
      keycloak
        .updateToken(30)
        .then((refreshed) => {
          if (refreshed) {
            console.log('Token refreshed')
          }
        })
        .catch(() => {
          console.log('Failed to refresh token')
        })
    }, 10000)

    createRoot(document.getElementById('root')).render(
      <StrictMode>
        <App keycloak={keycloak} />
      </StrictMode>,
    )
  })
  .catch((err) => {
    console.error('Keycloak init failed', err)
  })