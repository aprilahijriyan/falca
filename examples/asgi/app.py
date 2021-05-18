import os

from falcon.asgi.ws import WebSocket

from falca.responses import HTMLResponse

envvar = "FALCA_SETTINGS"
os.environ.setdefault(envvar, "settings")

from private.router import private_router
from resources.article import Article
from resources.home import Home
from resources.media import Media

from falca.app import ASGI

app = ASGI(__name__)
app.settings.from_envvar(envvar)


@app.cli.command("runserver")
def runserver():
    """
    Run it!!!
    """

    print("bakekok!")


@app.get("/")
async def index():
    return HTMLResponse("index.html", context={"body": "not bad!"})


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
