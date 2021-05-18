from falca.resource import Resource
from falca.responses import HTMLResponse


class Home(Resource):
    def on_get(self):
        """
        Test html templates
        """

        return HTMLResponse("index.html", context={"body": "not bad!"})
