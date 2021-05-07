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
        limit = query.data.get("limit")
        offset = query.data.get("offset")
        data = list(range(1, 11))[limit:offset]
        self.json({"data": data})

    def on_post(self, id):
        self.json({"data": 1})
