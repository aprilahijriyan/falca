from wsgiref import simple_server

from private.router import private_router
from resources.article import Article
from resources.home import Home
from resources.media import Media

from falca.app import WSGI

app = WSGI(__name__)
app.add_route("/", Home())
app.add_route("/article", Article())
app.add_route("/media", Media())
app.add_router(private_router)

if __name__ == "__main__":
    httpd = simple_server.make_server("127.0.0.1", 8000, app)
    httpd.serve_forever()
