from mimetypes import guess_type
from pathlib import Path

from pytest import mark

from falca.testing import TestClient


@mark.asyncio
async def test_media_upload(client: TestClient):
    filename = "mie_ayam.jpeg"
    path = Path("static") / filename
    files = {"file": (filename, open(path, "rb"), guess_type(filename)[0])}
    resp = await client.post("/media", files=files)
    assert resp.json["success"] == 1
