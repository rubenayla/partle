from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_parts():
    resp = client.get('/v1/parts/')
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    if data:
        assert 'name' in data[0]


def test_get_stores():
    resp = client.get('/v1/stores/')
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    if data:
        assert 'name' in data[0]
