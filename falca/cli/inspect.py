from typing import Union

from rich import print as cprint
from rich.tree import Tree
from typer import Context

from ..app import ASGI, WSGI


def parse_tree(tree: Tree, routes: list):
    pass


def get_routes(app: Union[WSGI, ASGI]):
    roots = app._router._roots
    routers = app.routers
    root = Tree(":bookmark_tabs: Resources", highlight=True)
    parse_tree(root, roots)
    for router in routers:
        roots = router._roots
        child = root.add(f":open_file_folder: {router.url_prefix}")
        parse_tree(child, roots)

    return root


def inspect_command(ctx: Context):
    """
    Inspect routes
    """

    tree = get_routes(ctx.app)
    cprint(tree)
