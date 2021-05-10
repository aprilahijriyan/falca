from marshmallow import fields

from falca.annotations import Body, Query
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


class Article(Resource):
    def on_get(self, query: limit_offset_query):
        self.json(query.data)

    def on_post(self, body: article_body):
        self.json(body.data)