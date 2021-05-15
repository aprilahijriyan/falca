from falca.resource import Resource
from falca.responses import HtmlResponse


class Home(Resource):
    def on_get(self):
        """
        Test html templates
        """

        return HtmlResponse("index.html", context={"body": "not bad!"})
