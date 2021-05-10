from marshmallow import fields

from falca.annotations import File
from falca.resource import Resource
from falca.schema import Schema


class MediaSchema(Schema):
    file = fields.Raw(required=True)


schema = File(MediaSchema())


class Media(Resource):
    def on_post(self, body: schema):
        print(body.data)
        self.json({"success": 1})
