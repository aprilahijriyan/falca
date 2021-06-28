def test_404(wsgi_client):
    resp = wsgi_client.get("/not-found")
    assert resp.json == {
        "status": {"code": 404, "description": "Not Found"},
        "link": None,
    }
