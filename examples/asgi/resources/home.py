from falca.resource import Resource
from falca.responses import HtmlResponse


class Home(Resource):
    async def on_get(self):
        return HtmlResponse("index.html", context={"body": "not bad!"})
