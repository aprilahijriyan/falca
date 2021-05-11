from mimetypes import guess_type
from pathlib import Path

from falcon.testing import TestClient
from requests_toolbelt import MultipartEncoder


def test_media_upload(client: TestClient):
    filename = "mie_ayam.jpeg"
    path = Path("static") / filename
    data = {"file": (filename, open(path, "rb"), guess_type(filename)[0])}
    encoder = MultipartEncoder(data)
    body = encoder.to_string()
    headers = {"Content-Type": encoder.content_type}
    resp = client.simulate_post("/media", body=body, headers=headers)
    assert resp.json["success"] == 1
