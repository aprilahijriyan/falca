from ..decorators import use_plugins
from ..resource import Resource


@use_plugins(["openapi"])
class RedocResource(Resource):
    def on_get(self):
        self.html(
            "redoc.html",
            dict(
                title=self.openapi.title,
                openapi_url=self.openapi.openapi_json,
                redoc_url=self.openapi.redoc_cdn,
            ),
        )


@use_plugins(["openapi"])
class OpenAPIResource(Resource):
    def on_get(self):
        self.json(self.openapi.to_json())


@use_plugins(["openapi"])
class SwaggerUIResource(Resource):
    def on_get(self):
        self.html(
            "swagger.html",
            dict(
                title=self.openapi.title,
                swagger_ui_url=self.openapi.swagger_cdn,
                openapi_url=self.openapi.openapi_json,
            ),
        )
