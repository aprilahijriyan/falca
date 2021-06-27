from falca.responses import JSONResponse


class Resource:
    def on_get(self, token: str):
        return JSONResponse({"token": token})


def test_path(wsgi_app, wsgi_client):
    wsgi_app.add_route("/test/{token}", Resource())
    resp = wsgi_client.get("/test/secret")
    assert resp.json["token"] == "secret"
