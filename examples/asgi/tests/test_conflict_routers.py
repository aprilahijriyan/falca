from app import app
from pytest import mark, raises

from falca.exceptions import BadRouter, EndpointConflict
from falca.resource import Resource
from falca.router import AsyncRouter


class Simple(Resource):
    async def on_get(self):
        pass


@mark.asyncio
async def test_bad_router():
    router = AsyncRouter()
    router.add_route("/api", Simple())
    with raises(BadRouter):
        app.include_router(router)


@mark.asyncio
async def test_conflict_endpoint():
    app.add_route("/simple", Simple())
    with raises(EndpointConflict):
        app.add_route("/simple", Simple())


@mark.asyncio
async def test_conflict_router():
    router = AsyncRouter(url_prefix="/simple")
    router.add_route("/api", Simple())
    app.include_router(router)
    with raises(EndpointConflict):
        app.include_router(router)
