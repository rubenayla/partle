import { useEffect, useState } from 'react'

export function useBackendStatus(): 'online' | 'offline' | 'checking' {
    const [status, setStatus] = useState<'online' | 'offline' | 'checking'>('checking')

    useEffect(() => {
        const controller = new AbortController()
        fetch(`${import.meta.env.VITE_API_BASE}/v1/health/`, { signal: controller.signal })
            .then(res => {
                if (!res.ok) throw new Error('Not OK')
                setStatus('online')
            })
            .catch(() => setStatus('offline'))

        return () => controller.abort()
    }, [])

    return status
}
