import asyncio

import pytest

from falca.responses import JSONResponse

data = [{"name": "kwoakwoakow", "email": "kwoakwoakow@land.com"}]

default = JSONResponse(data)


class Users:
    def on_get(self):
        return default


class AsyncUsers:
    async def on_get(self):
        await asyncio.sleep(5)
        return default


def test_resources_wsgi(wsgi_app, wsgi_client):
    wsgi_app.add_route("/users/class", Users())

    @wsgi_app.get("/users/function")
    def users_function():
        return default

    resp = wsgi_client.get("/users/class")
    assert resp.json == data
    resp = wsgi_client.get("/users/function")
    assert resp.json == data


@pytest.mark.asyncio
async def test_resources_asgi(asgi_app, asgi_client):
    asgi_app.add_route("/users/class", AsyncUsers())

    @asgi_app.get("/users/function")
    async def users_function():
        await asyncio.sleep(5)
        return default

    resp = await asgi_client.get("/users/class")
    assert resp.json == data
    resp = await asgi_client.get("/users/function")
    assert resp.json == data
