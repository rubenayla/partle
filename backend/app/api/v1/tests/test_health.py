def test_health_check(client, db):
    resp = client.get('/v1/health')
    assert resp.status_code == 200
    assert resp.json() == {'status': 'ok'}

