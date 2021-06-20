from falca.responses import HTMLResponse


class Home:
    async def on_get(self):
        return HTMLResponse("index.html", context={"body": "not bad!"})
