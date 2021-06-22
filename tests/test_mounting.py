from pytest import mark

from falca.app import ASGI, WSGI
from falca.responses import JSONResponse


def test_wsgi(wsgi_app, wsgi_client):
    def private():
        return JSONResponse({"status": 1})

    sub_app = WSGI(__name__)
    sub_app.add_route("/private", private, methods=["get"])
    wsgi_app.mount("/sub", sub_app)
    resp = wsgi_client.get("/sub/private")
    assert resp.json["status"] == 1

    nested_app = WSGI(__name__)
    nested_app.add_route("/status", private, methods=["get"])
    sub_app.mount("/nested", nested_app)
    resp = wsgi_client.get("/sub/nested/status")
    assert resp.json["status"] == 1


@mark.asyncio
async def test_asgi(asgi_app, asgi_client):
    async def private():
        return JSONResponse({"status": 1})

    sub_app = ASGI(__name__)
    sub_app.add_route("/private", private, methods=["get"])
    asgi_app.mount("/sub", sub_app)
    resp = await asgi_client.get("/sub/private")
    assert resp.json["status"] == 1

    nested_app = ASGI(__name__)
    nested_app.add_route("/status", private, methods=["get"])
    sub_app.mount("/nested", nested_app)
    resp = await asgi_client.get("/sub/nested/status")
    assert resp.json["status"] == 1
