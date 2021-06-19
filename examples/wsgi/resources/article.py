from marshmallow import fields

from falca.depends.marshmallow import Body, Form, Query
from falca.responses import JSONResponse
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
    def on_get(self, query: dict = Query(LimitOffsetSchema())):
        """
        Test query parameters
        """

        return JSONResponse(query)

    def on_post(self, body: dict = Body(ArticleSchema())):
        """
        Test json body
        """

        return JSONResponse(body)

    def on_post_form(self, form: dict = Form(ArticleSchema())):
        """
        Test form data with suffixes
        """

        return JSONResponse(form)
