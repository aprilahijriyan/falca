from mimetypes import guess_type
from pathlib import Path

from falcon.testing import TestClient
from pytest import mark
from requests_toolbelt import MultipartEncoder


@mark.asyncio
async def test_media_upload(client: TestClient):
    filename = "mie_ayam.jpeg"
    path = Path("static") / filename
    data = {"file": (filename, open(path, "rb"), guess_type(filename)[0])}
    encoder = MultipartEncoder(data)
    body = encoder.to_string()
    headers = {"Content-Type": encoder.content_type}
    resp = await client.simulate_post("/media", body=body, headers=headers)
    assert resp.json["success"] == 1
