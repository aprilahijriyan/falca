from apispec import APISpec
from falcon.app import App

from .resources import OpenAPIResource, RedocResource, SwaggerUIResource


class OpenAPI(APISpec):
    resources = {
        "openapi": OpenAPIResource,
        "redoc": RedocResource,
        "swagger_ui": SwaggerUIResource,
    }
    api_spec_options = {
        "info": {
            "description": "Powered by [falca](https://github.com/aprilahijriyan/falca)",
            "contact": {"email": "hijriyan23@gmail.com"},
            "license": {
                "name": "MIT License",
                "url": "https://wikipedia.org/wiki/Licence_MIT",
            },
        }
    }

    def __init__(self, app: App):
        settings = app.settings
        api_docs = settings.get("API_DOCS", True)
        title = settings.get("API_TITLE", "API Docs")
        version = settings.get("API_VERSION", "v1")
        openapi_version = settings.get("OPENAPI_VERSION", "3.0.2")
        options = settings.get("API_SPEC_OPTIONS", self.api_spec_options)
        self.openapi_json = settings.get("OPENAPI_JSON_PATH", "/openapi.json")
        self.redoc_path = settings.get("OPENAPI_REDOC_PATH", "/redoc")
        self.redoc_cdn = settings.get(
            "OPENAPI_REDOC_CDN",
            "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js",
        )
        self.swagger_path = settings.get("OPENAPI_SWAGGER_UI_PATH", "/docs")
        self.swagger_cdn = settings.get(
            "OPENAPI_SWAGGER_UI_CDN", "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
        )
        super().__init__(title, version, openapi_version, **options)
        security_def = settings.get("API_SECURITY_DEFINITIONS", {})
        for scheme, attrs in security_def.items():
            self.components.security_scheme(scheme, attrs)

        if api_docs:
            if self.swagger_path:
                app.add_route(self.swagger_path, self.resources["swagger_ui"])
                app.add_route(self.openapi_json, self.resources["openapi"])
                if self.redoc_path:
                    app.add_route(self.redoc_path, self.resources["redoc"])
