from falca.resource import Resource
from falca.responses import HTMLResponse


class Home(Resource):
    async def on_get(self):
        return HTMLResponse("index.html", context={"body": "not bad!"})
