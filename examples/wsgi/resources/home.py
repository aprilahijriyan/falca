from falca.responses import HTMLResponse


class Home:
    def on_get(self):
        """
        Test html templates
        """

        return HTMLResponse("index.html", context={"body": "not bad!"})
