from falcon.testing import TestClient


def test_get_users(client: TestClient):
    result = {
        "users": [
            {"email": "wakwaw@wkwk.com", "password": "123"},
            {"email": "admin@wkwk.com", "password": "1234"},
            {"email": "toktokpaket@wkwk.com", "password": "12345"},
        ]
    }
    resp = client.simulate_get("/private/users")
    assert resp.json == result
