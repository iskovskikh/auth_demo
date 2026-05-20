import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import './App.css'
import SecretPage from './SecretPage.jsx'

function App({ keycloak }) {

    const [showSecret, setShowSecret] = useState(false)

    if (showSecret) {
        return (
            <SecretPage keycloak={keycloak} onBack={() => setShowSecret(false)} />
        )
    }

  return (
    <div>
      <h1>
        Hello {keycloak.tokenParsed?.preferred_username}
      </h1>

      <p>Email: {keycloak.tokenParsed?.email}</p>

      <button onClick={() => keycloak.logout()}>
        Logout
      </button>

      <button onClick={() => setShowSecret(true)}>
        Get Secret
      </button>
    </div>
  )
}

export default App