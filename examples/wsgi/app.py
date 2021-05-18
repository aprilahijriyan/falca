import os

envvar = "FALCA_SETTINGS"
os.environ.setdefault(envvar, "settings")

from private.router import private_router
from resources.article import Article
from resources.home import Home
from resources.media import Media

from falca.app import WSGI
from falca.responses import HTMLResponse

app = WSGI(__name__)
app.settings.from_envvar(envvar)


@app.get("/")
def index():
    return HTMLResponse("index.html", context={"body": "not bad!"})


app.add_route("/home", Home())
app.add_route("/article", Article())
app.add_route("/form", Article(), suffix="form")
app.add_route("/media", Media())
app.include_router(private_router)
