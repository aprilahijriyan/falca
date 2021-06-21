from pytest import mark

from falca.responses import JSONResponse


def test_marshmallow(wsgi_app, wsgi_client):
    from marshmallow import fields

    from falca.depends.marshmallow import Body, Form, Query
    from falca.serializers.marshmallow import Schema

    class LimitOffsetSchema(Schema):
        limit = fields.Int()
        offset = fields.Int()

    class ArticleSchema(Schema):
        title = fields.Str(required=True)
        content = fields.Str(required=True)
        categories = fields.List(fields.Str())
        tags = fields.List(fields.Str())

    class Article:
        def on_get(self, query: dict = Query(LimitOffsetSchema)):
            """
            Test query parameters
            """

            return JSONResponse(query)

        def on_post(self, body: dict = Body(ArticleSchema)):
            """
            Test json body
            """

            return JSONResponse(body)

        def on_post_form(self, form: dict = Form(ArticleSchema)):
            """
            Test form data with suffixes
            """

            return JSONResponse(form)

    wsgi_app.add_route("/article", Article())
    wsgi_app.add_route("/form", Article(), suffix="form")

    def test_query():
        params = {"limit": 1, "offset": 1}
        resp = wsgi_client.get("/article", params=params)
        assert resp.json == params

    def test_json():
        json = {
            "title": "Awesome Falcon",
            "content": "Falcon is great framework!",
            "categories": ["Falcon", "On", "Fire!"],
            "tags": ["Satu", "Dua"],
        }
        resp = wsgi_client.post("/article", json=json)
        assert resp.json == json

    def test_form():
        data = {
            "title": "Awesome Falcon",
            "content": "Falcon is great framework!",
            "categories": ["Falcon", "On", "Fire!"],
            "tags": ["Satu", "Dua"],
        }
        resp = wsgi_client.post("/form", body=data)
        assert resp.json == data

    def test_error():
        params = {"limit": "oops", "offset": 1}
        resp = wsgi_client.get("/article", params=params)
        assert resp.json == {
            "status": {"code": 422, "description": "Unprocessable Entity"},
            "data": {"limit": ["Not a valid integer."]},
        }

    test_query()
    test_json()
    test_form()
    test_error()


@mark.asyncio
async def test_pydantic(asgi_app, asgi_client):
    from typing import List, Optional

    from falca.depends.pydantic import Body, Form, Query
    from falca.serializers.pydantic import Schema

    class LimitOffsetSchema(Schema):
        limit: Optional[int]
        offset: Optional[int]

    class ArticleSchema(Schema):
        title: str
        content: str
        categories: Optional[List[str]]
        tags: Optional[List[str]]

    class Article:
        async def on_get(self, query: dict = Query(LimitOffsetSchema)):
            return JSONResponse(query)

        async def on_post(self, body: dict = Body(ArticleSchema)):
            return JSONResponse(body)

        async def on_post_form(self, form: dict = Form(ArticleSchema)):
            """
            Test form data with suffixes
            """

            return JSONResponse(form)

    asgi_app.add_route("/article", Article())
    asgi_app.add_route("/form", Article(), suffix="form")

    async def test_query():
        params = {"limit": 1, "offset": 1}
        resp = await asgi_client.get("/article", params=params)
        assert resp.json == params

    async def test_json():
        json = {
            "title": "Awesome Falcon",
            "content": "Falcon is great framework!",
            "categories": ["Falcon", "On", "Fire!"],
            "tags": ["Satu", "Dua"],
        }
        resp = await asgi_client.post("/article", json=json)
        assert resp.json == json

    async def test_form():
        data = {
            "title": "Awesome Falcon",
            "content": "Falcon is great framework!",
            "categories": ["Falcon", "On", "Fire!"],
            "tags": ["Satu", "Dua"],
        }
        resp = await asgi_client.post("/form", body=data)
        assert resp.json == data

    async def test_error():
        params = {"limit": "oops", "offset": 1}
        resp = await asgi_client.get("/article", params=params)
        assert resp.json == {
            "data": [
                {
                    "loc": ["limit"],
                    "msg": "value is not a valid integer",
                    "type": "type_error.integer",
                }
            ],
            "status": {"code": 422, "description": "Unprocessable Entity"},
        }

    await test_query()
    await test_json()
    await test_form()
    await test_error()
