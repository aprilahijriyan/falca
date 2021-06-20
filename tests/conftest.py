import pytest

from falca.app import ASGI, WSGI
from falca.testing import TestClient

cache = {}


def create_or_get(key, klass):
    app = cache.get(key, None)
    if app is None:
        app = klass(__name__)
        cache[key] = app
    return app


@pytest.fixture
def asgi_app():
    return create_or_get("asgi_app", ASGI)


@pytest.fixture
def wsgi_app():
    return create_or_get("wsgi_app", WSGI)


@pytest.fixture
@pytest.mark.asyncio
async def asgi_client(asgi_app):
    client = TestClient(asgi_app)
    async with client as conductor:
        yield conductor


@pytest.fixture
def wsgi_client(wsgi_app):
    client = TestClient(wsgi_app)
    return client
