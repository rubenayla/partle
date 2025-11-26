def test_health_check(client, db):
    resp = client.get('/v1/health')
    assert resp.status_code == 200
    payload = resp.json()
    assert payload['status'] in {'ok', 'degraded'}
    assert set(payload['environment'].keys()) == {
        'DATABASE_URL',
        'SECRET_KEY',
        'CLOUDFLARE_WORKER_URL',
        'CLOUDFLARE_WORKER_API_KEY',
    }
    assert isinstance(payload.get('warnings'), list)
