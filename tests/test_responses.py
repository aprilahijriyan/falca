from pathlib import Path

from falcon.constants import MEDIA_HTML, MEDIA_JSON, MEDIA_TEXT
from pytest import mark

from falca.responses import FileResponse, HTMLResponse, JSONResponse, TextResponse


class JSONResource:
    def on_get(self):
        return JSONResponse({"status": 1})


class HTMLResource:
    def on_get(self):
        return HTMLResponse("index.html")


class TextResource:
    def on_get(self):
        return TextResponse("text doang")


class FileResource:
    async def on_get(self):
        path = Path("tests/templates") / "index.html"
        content = path.read_text()
        return FileResponse("index.html", content)


class StreamingResource:
    async def on_get(self):
        path = Path("tests/templates") / "index.html"
        fp = path.open("rb")

        async def gen_content():
            while True:
                line = fp.readline()
                if not line:
                    break
                yield line
            yield b""

        return FileResponse("index.html", gen_content())


def test_json(wsgi_app, wsgi_client):
    wsgi_app.add_route("/json", JSONResource())
    resp = wsgi_client.get("/json")
    assert resp.headers["content-type"] == MEDIA_JSON
    assert resp.json["status"] == 1


def test_html(wsgi_app, wsgi_client):
    wsgi_app.add_route("/html", HTMLResource())
    resp = wsgi_client.get("/html")
    assert resp.headers["content-type"] == MEDIA_HTML
    assert "hey hey not bad" in resp.text


def test_text(wsgi_app, wsgi_client):
    wsgi_app.add_route("/text", TextResource())
    resp = wsgi_client.get("/text")
    assert resp.headers["content-type"] == MEDIA_TEXT
    assert resp.text == "text doang"


@mark.asyncio
async def test_file(asgi_app, asgi_client):
    asgi_app.add_route("/file-download", FileResource())
    resp = await asgi_client.get("/file-download")
    assert resp.headers["content-type"] in MEDIA_HTML
    async with asgi_client.get_stream("/file-download") as sr:
        fp = Path("tests/templates/index_copy.html").open("wb")
        with fp:
            while True:
                chunk = await sr.stream.read()
                if not chunk:
                    break
                fp.write(chunk)


@mark.asyncio
async def test_file_stream(asgi_app, asgi_client):
    asgi_app.add_route("/file-stream", StreamingResource())
    resp = await asgi_client.get("/file-stream")
    assert resp.headers["content-type"] in MEDIA_HTML
    async with asgi_client.get_stream("/file-stream") as sr:
        fp = Path("tests/templates/index_stream.html").open("wb")
        with fp:
            while True:
                chunk = await sr.stream.read()
                if not chunk:
                    break
                fp.write(chunk)
