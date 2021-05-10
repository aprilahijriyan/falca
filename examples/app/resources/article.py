from marshmallow import fields

from falca.annotations import Query
from falca.resource import Resource
from falca.schema import Schema


class LimitOffsetSchema(Schema):
    limit = fields.Int()
    offset = fields.Int()


limit_offset_query = Query(LimitOffsetSchema())


class Article(Resource):
    def on_get(self, query: limit_offset_query):
        self.json(query.data)

    def on_post(self):
        self.json({"data": 1})
