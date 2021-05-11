from falcon.testing import TestClient
from pytest import mark


@mark.asyncio
async def test_get_article(client: TestClient):
    params = {"limit": 1, "offset": 1}
    resp = await client.simulate_get("/article", params=params)
    assert resp.json == params


@mark.asyncio
async def test_post_article(client: TestClient):
    json = {
        "title": "Awesome Falcon",
        "content": "Falcon is great framework!",
        "categories": ["Falcon", "On", "Fire!"],
        "tags": ["Satu", "Dua"],
    }
    resp = await client.simulate_post("/article", json=json)
    assert resp.json == json