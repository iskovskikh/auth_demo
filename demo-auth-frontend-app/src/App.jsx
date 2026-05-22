import { useEffect, useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import './App.css'
import SecretPage from './SecretPage.jsx'

function App({ keycloak }) {

    const [showSecret, setShowSecret] = useState(false)

    const [data, setData] = useState(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)

    useEffect(() => {
        const url = import.meta.env.VITE_BASE_URL + 'auth/profile'
        const headers = {
            Authorization: 'Bearer ' + keycloak.token,
            Accept: 'application/json',
        }
        fetch(url, { headers })
        .then((resp) => {
            if (!resp.ok) {
                throw new Error('HTTP ' + resp.status)
            }
            return resp.json()
        })
        .then((json) => {
             setData(json)
             setLoading(false)
        })
        .catch((err) => {
             setError(err.message)
             setLoading(false)
        })
    }, [keycloak.token])


    if (showSecret) {
        return (
            <SecretPage keycloak={keycloak} onBack={() => setShowSecret(false)} />
        )
    }

    return (
        <div class="layout">
            <h1>Main Page</h1>
            <div>
                <h2>Token info</h2>
                <p>username: {keycloak.tokenParsed?.preferred_username}</p>
                <p>Email: {keycloak.tokenParsed?.email}</p>
            </div>

            <div>
                <h2>Profile info</h2>
                {loading && <p>Loading profile…</p>}
                {error && <p style={{ color: 'red' }}>{error}</p>}
                {data && <pre>{JSON.stringify(data, null, 2)}</pre>}
            </div>

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