import os

envvar = "FALCA_SETTINGS"
os.environ.setdefault(envvar, "settings")

from plugin import Logger
from private.router import private_router
from resources.article import Article
from resources.home import Home
from resources.media import Media

from falca.app import WSGI
from falca.depends import Plugin, Settings
from falca.responses import HTMLResponse, JSONResponse

app = WSGI(__name__)
app.settings.from_envvar(envvar)
app.plugins.install("plugin.Logger")


@app.get("/")
def index(logger: Logger = Plugin("logging")):
    logger.info("are you ok ?")
    return HTMLResponse("index.html", context={"body": "not bad!"})


@app.get("/settings")
def settings(part_config: dict = Settings("part_config")):
    return JSONResponse(part_config)


app.add_route("/home", Home())
app.add_route("/article", Article())
app.add_route("/form", Article(), suffix="form")
app.add_route("/media", Media())
app.include_router(private_router)
