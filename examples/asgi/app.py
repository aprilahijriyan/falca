from private.router import private_router
from resources.article import Article
from resources.home import Home
from resources.media import Media

from falca.app import ASGI

app = ASGI(__name__)
app.add_route("/", Home())
app.add_route("/article", Article())
app.add_route("/media", Media())
app.add_router(private_router)
