from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    resp = client.get('/v1/health')
    assert resp.status_code == 200
    assert resp.json() == {'status': 'ok'}

