def test_get_parts(client, db):
    resp = client.get("/v1/parts/")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    if data:
        assert "name" in data[0]


def test_get_stores(client, db):
    resp = client.get("/v1/stores/")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    if data:
        assert "name" in data[0]
