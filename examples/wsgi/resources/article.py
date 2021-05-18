from marshmallow import fields

from falca.annotations import Body, Form, Query
from falca.resource import Resource
from falca.responses import JSONResponse
from falca.schema import Schema


class LimitOffsetSchema(Schema):
    limit = fields.Int()
    offset = fields.Int()


class ArticleSchema(Schema):
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    categories = fields.List(fields.Str())
    tags = fields.List(fields.Str())


limit_offset_query = Query(LimitOffsetSchema())
article_body = Body(ArticleSchema())
article_form = Form(ArticleSchema())


class Article(Resource):
    def on_get(self, query: limit_offset_query):
        """
        Test query parameters
        """

        return JSONResponse(query.data)

    def on_post(self, body: article_body):
        """
        Test json body
        """

        return JSONResponse(body.data)

    def on_post_form(self, form: article_form):
        """
        Test form data with suffixes
        """

        return JSONResponse(form.data)
