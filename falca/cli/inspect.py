from typing import List, Union

from falcon.routing.compiled import CompiledRouterNode
from rich import print as cprint
from rich.table import Table
from rich.tree import Tree
from typer import Context

from ..app import ASGI, WSGI


def parse_tree(tree: Tree, routes: List[CompiledRouterNode], *, prefix: str = None):
    for node in routes:
        resource = type(node.resource).__name__
        endpoint = node.uri_template
        if prefix:
            endpoint = "/" + endpoint.lstrip(prefix)

        method_map = node.method_map
        child = tree.add(f":bookmark_tabs:  {endpoint} ({resource})", highlight=True)
        table = Table(show_lines=True)
        table.add_column("Method")
        table.add_column("Description")
        for method, responder in method_map.items():
            doc = (responder.__doc__ or "").strip("\n")
            name = responder.__name__
            if name.startswith("on_"):
                table.add_row(method, doc)

        child.add(table)


def get_routes(app: Union[WSGI, ASGI]):
    roots = app._router._roots
    routers = app._router.children
    root = Tree(":bookmark_tabs: Resources", highlight=True)
    parse_tree(root, roots)
    for router in routers:
        roots = router._roots
        prefix = router.url_prefix
        for node in roots:
            child = root.add(f":open_file_folder: {prefix}")
            parse_tree(child, node.children, prefix=prefix)

    return root


def inspect_command(ctx: Context):
    """
    Inspect routes
    """

    tree = get_routes(ctx.obj)
    cprint(tree)
