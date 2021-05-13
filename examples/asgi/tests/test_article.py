from pytest import mark

from falca.testing import TestClient


@mark.asyncio
async def test_get_article(client: TestClient):
    params = {"limit": 1, "offset": 1}
    resp = await client.get("/article", params=params)
    assert resp.json == params


@mark.asyncio
async def test_post_article(client: TestClient):
    json = {
        "title": "Awesome Falcon",
        "content": "Falcon is great framework!",
        "categories": ["Falcon", "On", "Fire!"],
        "tags": ["Satu", "Dua"],
    }
    resp = await client.post("/article", json=json)
    assert resp.json == json


@mark.asyncio
async def test_form_article(client: TestClient):
    data = {
        "title": "Awesome Falcon",
        "content": "Falcon is great framework!",
        "categories": ["Falcon", "On", "Fire!"],
        "tags": ["Satu", "Dua"],
    }
    resp = await client.post("/form", body=data)
    assert resp.json == data
