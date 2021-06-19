from app import app
from pytest import raises

from falca.exceptions import BadRouter, EndpointConflict
from falca.router import Router


class Simple:
    def on_get(self):
        pass


def test_bad_router():
    router = Router()
    router.add_route("/api", Simple())
    with raises(BadRouter):
        app.include_router(router)


def test_conflict_endpoint():
    app.add_route("/simple", Simple())
    with raises(EndpointConflict):
        app.add_route("/simple", Simple())


def test_conflict_router():
    router = Router(url_prefix="/simple")
    router.add_route("/api", Simple())
    app.include_router(router)
    with raises(EndpointConflict):
        app.include_router(router)
