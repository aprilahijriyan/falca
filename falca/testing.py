from typing import Optional, Type, Union
from urllib.parse import urlencode

from falcon.constants import MEDIA_URLENCODED
from falcon.errors import CompatibilityError
from falcon.testing import ASGIConductor as _ASGIConductor
from falcon.testing import Result
from falcon.testing import TestClient as _TestClient
from falcon.testing.client import _is_asgi_app
from requests_toolbelt import MultipartEncoder

from .app import ASGI, WSGI


def _fix_request_body(kwargs: dict):
    body = kwargs.pop("body", None)
    files = kwargs.pop("files", None)
    content_type = None
    if isinstance(body, dict) and not files:
        content_type = MEDIA_URLENCODED
        body = urlencode(body, True)

    if isinstance(files, dict):
        if isinstance(body, dict):
            body.update(files)
        else:
            body = files

        encoder = MultipartEncoder(body)
        content_type = encoder.content_type
        body = encoder.to_string()

    headers = kwargs.get("headers", {})
    if content_type:
        headers["Content-Type"] = content_type

    kwargs["headers"] = headers
    if body:
        kwargs["body"] = body


class ASGIConductor(_ASGIConductor):
    def __init__(self, app: Union[WSGI, ASGI], headers: dict = None):
        super().__init__(app, headers=headers)

    async def simulate_request(self, *args, **kwargs) -> Result:
        _fix_request_body(kwargs)
        return await super().simulate_request(*args, **kwargs)

    # flavor
    get = _ASGIConductor.simulate_get
    get_stream = _ASGIConductor.simulate_get_stream
    post = _ASGIConductor.simulate_post
    put = _ASGIConductor.simulate_put
    patch = _ASGIConductor.simulate_patch
    head = _ASGIConductor.simulate_head
    options = _ASGIConductor.simulate_options
    delete = _ASGIConductor.simulate_delete
    ws = _ASGIConductor.simulate_ws
    request = simulate_request


class TestClient(_TestClient):
    def __init__(
        self,
        app: Union[WSGI, ASGI],
        headers: Optional[dict] = None,
        conductor_class: Type[ASGIConductor] = ASGIConductor,
    ):
        klass = type(app)
        assert (
            klass is WSGI or klass is ASGI
        ), "The app must be an instance object of falca.app.WSGI or falca.app.ASGI"

        if headers:
            assert isinstance(headers, dict), "The headers must be of type dict"

        assert conductor_class and issubclass(
            conductor_class, ASGIConductor
        ), "The conductor must be a sub-class of falca.testing.ASGIConductor"
        super().__init__(app, headers=headers)
        self._conductor_class = conductor_class

    async def __aenter__(self):
        if not _is_asgi_app(self.app):
            raise CompatibilityError(
                "a conductor context manager may only be used with a Falcon ASGI app"
            )

        # NOTE(kgriffs): We normally do not expect someone to try to nest
        #   contexts, so this is just a sanity-check.
        assert not self._conductor

        # Let us custom the conductor
        self._conductor = self._conductor_class(self.app, headers=self._default_headers)
        await self._conductor.__aenter__()

        return self._conductor

    def simulate_request(self, *args, **kwargs) -> Result:
        _fix_request_body(kwargs)
        return super().simulate_request(*args, **kwargs)

    # flavor
    get = _TestClient.simulate_get
    post = _TestClient.simulate_post
    put = _TestClient.simulate_put
    patch = _TestClient.simulate_patch
    head = _TestClient.simulate_head
    options = _TestClient.simulate_options
    delete = _TestClient.simulate_delete
    request = simulate_request
