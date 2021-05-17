from pytest import mark

from falca.testing import ASGIConductor


@mark.asyncio
async def test_ws(client: ASGIConductor):
    async with client.ws("/events") as ws:
        await ws.send_json({"key": "baka"})
        resp = await ws.receive_json()
        assert resp["msg"] == "ok"
