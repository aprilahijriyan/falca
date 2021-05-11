from falcon.testing import TestClient
from pytest import mark


@mark.asyncio
async def test_get_users(client: TestClient):
    result = {
        "users": [
            {"email": "wakwaw@wkwk.com", "password": "123"},
            {"email": "admin@wkwk.com", "password": "1234"},
            {"email": "toktokpaket@wkwk.com", "password": "12345"},
        ]
    }
    resp = await client.simulate_get("/private/users")
    assert resp.json == result
