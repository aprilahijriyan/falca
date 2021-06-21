from falcon.asgi.ws import WebSocket
from pytest import mark


@mark.asyncio
async def test_ws(asgi_app, asgi_client):
    @asgi_app.websocket("/events")
    async def events(ws: WebSocket):
        await ws.accept()
        data = await ws.receive_media()
        key = data["key"]
        msg = "ok" if key == "baka" else "oh"
        await ws.send_media({"msg": msg})

    async with asgi_client.ws("/events") as ws:
        await ws.send_json({"key": "baka"})
        resp = await ws.receive_json()
        assert resp["msg"] == "ok"
