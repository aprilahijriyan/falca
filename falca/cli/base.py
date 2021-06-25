import os
import sys
from typing import Any, Callable, Dict, Optional, Type

import click
from pkg_resources import get_distribution, iter_entry_points
from rich import print as cprint
from typer import Context, Exit, Option, Typer
from typer.models import Default

from ..exceptions import FalcaError
from ..helpers import import_attr
from .inspect import inspect_command
from .runserver import runserver_command
from .shell import shell_command


class Command(Typer):
    def __init__(
        self,
        *,
        name: Optional[str] = Default(None),
        cls: Optional[Type[click.Command]] = Default(None),
        # invoke_without_command: bool = Default(False),
        # no_args_is_help: Optional[bool] = Default(None),
        subcommand_metavar: Optional[str] = Default(None),
        chain: bool = Default(False),
        result_callback: Optional[Callable[..., Any]] = Default(None),
        # Command
        context_settings: Optional[Dict[Any, Any]] = Default(None),
        # callback: Optional[Callable[..., Any]] = Default(None),
        help: Optional[str] = Default(None),
        epilog: Optional[str] = Default(None),
        short_help: Optional[str] = Default(None),
        options_metavar: str = Default("[OPTIONS]"),
        add_help_option: bool = Default(True),
        hidden: bool = Default(False),
        deprecated: bool = Default(False),
        add_completion: bool = True,
    ):
        no_args_is_help = invoke_without_command = True
        callback = self.init
        super().__init__(
            name=name,
            cls=cls,
            invoke_without_command=invoke_without_command,
            no_args_is_help=no_args_is_help,
            subcommand_metavar=subcommand_metavar,
            chain=chain,
            result_callback=result_callback,
            context_settings=context_settings,
            callback=callback,
            help=help,
            epilog=epilog,
            short_help=short_help,
            options_metavar=options_metavar,
            add_help_option=add_help_option,
            hidden=hidden,
            deprecated=deprecated,
            add_completion=add_completion,
        )
        self.install_default_commands()
        for ep in iter_entry_points("falca.commands"):
            cmd = ep.load()
            if isinstance(cmd, Typer):
                self.add_typer(cmd)
            else:
                self.command(ep.name)(cmd)

        self.app = self.load_app()
        self.merge(self.app.cli)

    def merge(self, typer: Typer):
        for cmd in typer.registered_commands:
            for idx, old in enumerate(self.registered_commands):
                if old.name == cmd.name:
                    self.registered_commands[idx] = cmd
                    break

        for group in typer.registered_groups:
            for idx, old in enumerate(self.registered_groups):
                if old.name == group.name:
                    self.registered_groups[idx] = group
                    break

    def install_default_commands(self):
        self.command("inspect")(inspect_command)
        self.command("runserver")(runserver_command)
        self.command(
            "shell",
            context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
        )(shell_command)

    def load_app(self):
        from ..app import ASGI, WSGI

        try:
            os.chdir(os.getcwd())
            sys.path.insert(0, os.getcwd())
            src = os.environ.get("FALCA_APP", "app.app")
            app = import_attr(src)
            if callable(app):
                app = app()

            if not isinstance(app, (WSGI, ASGI)):
                raise FalcaError(f"Invalid application type {app!r}")

            return app

        except ImportError:
            cprint("[red]Error:[/red] can't find app :eyes:")
            raise Exit

    def init(
        self,
        ctx: Context,
        version: Optional[bool] = Option(
            None, "--version", is_eager=True, help="Show version number and exit"
        ),
    ):

        if ctx.resilient_parsing:
            return

        if version:
            v = get_distribution("falca").version
            cprint(f":package: Falca v{v}")
            raise Exit

        ctx.obj = self.app
