from typing import List, Optional

from falca.depends.pydantic import Body, Form, Query
from falca.resource import Resource
from falca.responses import JSONResponse
from falca.serializers.pydantic import Schema


class LimitOffsetSchema(Schema):
    limit: Optional[int]
    offset: Optional[int]


class ArticleSchema(Schema):
    title: str
    content: str
    categories: Optional[List[str]]
    tags: Optional[List[str]]


class Article(Resource):
    async def on_get(self, query: dict = Query(LimitOffsetSchema)):
        return JSONResponse(query)

    async def on_post(self, body: dict = Body(ArticleSchema)):
        return JSONResponse(body)

    async def on_post_form(self, form: dict = Form(ArticleSchema)):
        """
        Test form data with suffixes
        """

        return JSONResponse(form)
