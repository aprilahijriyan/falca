from marshmallow import fields

from falca.annotations import Body, Form, Query
from falca.resource import Resource
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
    async def on_get(self, query: limit_offset_query):
        self.json(query.data)

    async def on_post(self, body: article_body):
        self.json(body.data)

    async def on_post_form(self, form: article_form):
        """
        Test form data with suffixes
        """

        self.json(form.data)
