from falca.resource import Resource


class Home(Resource):
    def on_get(self):
        self.html("index.html", context={"body": "not bad!"})