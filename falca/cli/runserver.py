from rich import print as cprint
from typer import Context, Option

from ..app import ASGI, WSGI


def runserver_command(
    ctx: Context,
    host: str = Option("127.0.0.1", help="Hostname"),
    port: int = Option(9999, help="Port"),
):
    """
    Run the application
    """

    app = ctx.obj
    if isinstance(app, ASGI):
        try:
            from uvicorn import run

            run(app, host=host, port=port)

        except ImportError:
            cprint(
                "[red]Error[/red]: ASGI application detected. Please install [bold][i]uvicorn[/i][/bold] first to run the application."
            )

    elif isinstance(app, WSGI):
        try:
            from gunicorn.app.base import BaseApplication

            class WSGIWrapper(BaseApplication):
                def __init__(self, host, port, options={}):
                    options["bind"] = "%s:%s" % (host, port)
                    self.options = options
                    super().__init__()

                def load_config(self):
                    config = {
                        key: value
                        for key, value in self.options.items()
                        if key in self.cfg.settings and value is not None
                    }
                    for key, value in config.items():
                        self.cfg.set(key.lower(), value)

                def load(self):
                    return app

            WSGIWrapper(host, port).run()

        except ImportError:
            from wsgiref.simple_server import make_server

            cprint(f"Listening at: [bold]http://{host}:{port}[/bold]")
            httpd = make_server(host, port, app)
            httpd.serve_forever()

    else:
        cprint("[red]Error[/red]: unknown application")
