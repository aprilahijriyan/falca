from wsgiref import simple_server

from resources.article import Article

from falca.app import WSGI

app = WSGI(__name__)
app.add_route("/article", Article)

if __name__ == "__main__":
    httpd = simple_server.make_server("127.0.0.1", 8000, app)
    httpd.serve_forever()
