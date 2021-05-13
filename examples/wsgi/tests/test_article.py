from falca.testing import TestClient


def test_get_article(client: TestClient):
    params = {"limit": 1, "offset": 1}
    resp = client.get("/article", params=params)
    assert resp.json == params


def test_post_article(client: TestClient):
    json = {
        "title": "Awesome Falcon",
        "content": "Falcon is great framework!",
        "categories": ["Falcon", "On", "Fire!"],
        "tags": ["Satu", "Dua"],
    }
    resp = client.post("/article", json=json)
    assert resp.json == json


def test_form_article(client: TestClient):
    data = {
        "title": "Awesome Falcon",
        "content": "Falcon is great framework!",
        "categories": ["Falcon", "On", "Fire!"],
        "tags": ["Satu", "Dua"],
    }
    resp = client.post("/form", body=data)
    assert resp.json == data
