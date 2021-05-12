from falca.resource import Resource


class Home(Resource):
    def on_get(self):
        """
        Test html templates
        """

        self.html("index.html", context={"body": "not bad!"})
