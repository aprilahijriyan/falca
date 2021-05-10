from wsgiref import simple_server

from resources.article import Article

from falca.app import WSGI
from falca.resource import Resource


class Home(Resource):
    def on_get(self, id):
        print("")
        self.json({"hello": "world " + id})


# app = App()
app = WSGI(__name__)
app.add_route("/{id}", Home())
app.add_route("/test", Home())
app.add_route("/article", Article())

if __name__ == "__main__":
    httpd = simple_server.make_server("127.0.0.1", 8000, app)
    httpd.serve_forever()
