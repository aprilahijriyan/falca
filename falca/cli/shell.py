import sys

import IPython
from IPython.terminal.ipapp import load_default_config
from traitlets.config.loader import Config
from typer import Context


def shell_command(ctx: Context):
    """
    Run shell
    """

    # Based on https://github.com/ei-grad/flask-shell-ipython
    app = ctx.obj
    if "IPYTHON_CONFIG" in app.settings:
        config = Config(app.settings["IPYTHON_CONFIG"])
    else:
        config = load_default_config()

    config.TerminalInteractiveShell.banner1 = """
Python %s on %s
IPython: %s
App: %s [%s]
Instance: %s
        """ % (
        sys.version,
        sys.platform,
        IPython.__version__,
        type(app).__name__,
        app.import_name,
        app.root_path,
    )

    sys.argv[0] = sys.argv[0] + " shell"
    IPython.start_ipython(
        argv=ctx.args,
        user_ns=app.make_shell_context(),
        config=config,
    )
