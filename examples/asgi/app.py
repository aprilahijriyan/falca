import os

from falcon.asgi.ws import WebSocket

from falca.responses import HTMLResponse, JSONResponse

envvar = "FALCA_SETTINGS"
os.environ.setdefault(envvar, "settings")

from plugin import Logger
from private.router import private_router
from resources.article import Article
from resources.home import Home
from resources.media import Media

from falca.app import ASGI
from falca.depends import Plugin, Settings

app = ASGI(__name__)
app.settings.from_envvar(envvar)
app.plugins.install("plugin.Logger")


@app.get("/")
async def index(logger: Logger = Plugin("logging")):
    logger.info("are you ok ?")
    return HTMLResponse("index.html", context={"body": "not bad!"})


@app.get("/settings")
async def settings(part_config: dict = Settings("part_config")):
    return JSONResponse(part_config)


@app.websocket("/events")
async def events(ws: WebSocket):
    await ws.accept()
    data = await ws.receive_media()
    key = data["key"]
    msg = "ok" if key == "baka" else "oh"
    await ws.send_media({"msg": msg})


app.add_route("/home", Home())
app.add_route("/article", Article())
app.add_route("/form", Article(), suffix="form")
app.add_route("/media", Media())
app.include_router(private_router)
