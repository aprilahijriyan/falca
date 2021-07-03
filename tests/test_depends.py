import logging
from typing import Union

from marshmallow import fields, validate

from falca.app import ASGI, WSGI
from falca.depends import Plugin, Settings
from falca.depends.base import Depends
from falca.depends.marshmallow import Body, Query
from falca.plugins.base import BasePlugin
from falca.request import Request
from falca.responses import JSONResponse
from falca.serializers.marshmallow import Schema

LimitOffsetSchema = {"limit": fields.Int(), "offset": fields.Int()}


class ArticleSchema(Schema):
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    categories = fields.List(fields.Str())
    tags = fields.List(fields.Str())


class Logger(BasePlugin):
    name = "logging"

    def __init__(self, app: Union[WSGI, ASGI]) -> None:
        super().__init__(app)
        logging.basicConfig(level=logging.INFO)
        self._log = logging.getLogger(app.import_name)

    def info(self, *args, **kwds):
        self._log.info(*args, **kwds)

    def error(self, *args, **kwds):
        self._log.error(*args, **kwds)

    def warning(self, *args, **kwds):
        self._log.warning(*args, **kwds)

    def exception(self, *args, **kwds):
        self._log.exception(*args, **kwds)

    def debug(self, *args, **kwds):
        self._log.debug(*args, **kwds)


def test_plugin(wsgi_app, wsgi_client, caplog):
    class Resource:
        def on_get(self, log: Logger = Plugin("logging")):
            log.info("can you see me?")

    wsgi_app.plugins.install(Logger)
    wsgi_app.add_route("/plugins", Resource())
    with caplog.at_level(logging.INFO):
        wsgi_client.get("/plugins")

    assert "can you see me?" in caplog.text


def test_settings(wsgi_app, wsgi_client):
    class Resource:
        def on_get(self, config: dict = Settings()):
            return JSONResponse(config)

    wsgi_app.add_route("/settings", Resource())
    resp = wsgi_client.get("/settings")
    assert isinstance(resp.json, dict)

    class Resource:
        def on_get(self, foo: int = Settings("foo")):
            return JSONResponse({"foo": foo})

    wsgi_app.settings["foo"] = 1
    wsgi_app.add_route("/settings/foo", Resource())
    resp = wsgi_client.get("/settings/foo")
    assert resp.json["foo"] == 1


def test_function(wsgi_app, wsgi_client):
    def get_kebab_size(req: Request):
        size = req.params.get("size", "jumbo")
        return size

    class Resource:
        def on_get(self, kebab_size: str = Depends(get_kebab_size)):
            return JSONResponse({"kebab_size": kebab_size})

    wsgi_app.add_route("/order_kebab", Resource())
    resp = wsgi_client.get("/order_kebab?size=small")
    assert resp.json["kebab_size"] == "small"
    resp = wsgi_client.get("/order_kebab")
    assert resp.json["kebab_size"] == "jumbo"


def test_mix(wsgi_app, wsgi_client, caplog):
    class KebabSchema(Schema):
        size = fields.String(validate=validate.OneOf(["small", "medium", "jumbo"]))

    def get_kebab_size(req: Request, query: dict = Query(KebabSchema)):
        size = query.get("size", "jumbo")
        return size

    class Resource:
        def on_get(
            self,
            path: str,
            log: Logger = Plugin("logging"),
            foo: int = Settings("foo"),
            kebab_size: str = Depends(get_kebab_size),
        ):
            log.info("can you see me?")
            return JSONResponse({"path": path, "foo": foo, "kebab_size": kebab_size})

        def on_post(
            self,
            path: str,
            query: dict = Query(LimitOffsetSchema),
            body: dict = Body(ArticleSchema()),
        ):
            """
            Test json body
            """

            return JSONResponse({"path": path, "query": query, "body": body})

    wsgi_app.settings["foo"] = 1
    wsgi_app.add_route("/depends/mix/{path}", Resource())
    with caplog.at_level(logging.INFO):
        resp = wsgi_client.get("/depends/mix/wohoo?size=small")
        assert resp.json["path"] == "wohoo"
        assert resp.json["foo"] == 1
        assert resp.json["kebab_size"] == "small"
        resp = wsgi_client.get("/depends/mix/wohoo")
        assert resp.json["kebab_size"] == "jumbo"

    assert "can you see me?" in caplog.text
    resp = wsgi_client.get("/depends/mix/wohoo?size=invalid")
    assert resp.json == {
        "status": {"code": 422, "description": "Unprocessable Entity"},
        "data": {"size": ["Must be one of: small, medium, jumbo."]},
    }
    json = {
        "title": "Awesome Falcon",
        "content": "Falcon is great framework!",
        "categories": ["Falcon", "On", "Fire!"],
        "tags": ["Satu", "Dua"],
    }
    resp = wsgi_client.post("/depends/mix/wohoo?limit=100&offset=0", json=json)
    assert resp.json["path"] == "wohoo"
    assert resp.json["query"] == {"limit": 100, "offset": 0}
    assert resp.json["body"] == json
