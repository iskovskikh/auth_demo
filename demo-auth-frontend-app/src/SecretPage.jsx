import { useEffect, useState } from 'react'

function SecretPage({ keycloak, onBack }) {

    const [data, setData] = useState(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)

    useEffect(() => {
        const url = import.meta.env.VITE_BASE_URL + 'secret'
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

    return (
        <div class="layout">
            <h1>Secret Page</h1>
            {loading && <p>Loading secret…</p>}
            {error && <p style={{ color: 'red' }}>{error}</p>}
            {data && <pre>{JSON.stringify(data, null, 2)}</pre>}
            <button onClick={onBack}>Back</button>
        </div>
    )
}

export default SecretPage

