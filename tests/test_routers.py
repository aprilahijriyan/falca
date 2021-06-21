from pytest import raises

from falca.exceptions import BadRouter, EndpointConflict
from falca.responses import JSONResponse
from falca.router import Router


class Simple:
    def on_get(self):
        return JSONResponse({"status": 1})


def test_nested_router(wsgi_app, wsgi_client):
    router = Router(url_prefix="/nested")
    router.add_route("/simple", Simple())
    wsgi_app.include_router(router)
    resp = wsgi_client.get("/nested/simple")
    assert resp.json["status"] == 1


def test_bad_router(wsgi_app):
    router = Router()
    router.add_route("/api", Simple())
    with raises(BadRouter):
        wsgi_app.include_router(router)


def test_conflict_endpoint(wsgi_app):
    wsgi_app.add_route("/simple", Simple())
    with raises(EndpointConflict):
        wsgi_app.add_route("/simple", Simple())


def test_conflict_router(wsgi_app):
    router = Router(url_prefix="/simple")
    router.add_route("/api", Simple())
    wsgi_app.include_router(router)
    with raises(EndpointConflict):
        wsgi_app.include_router(router)
