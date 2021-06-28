from os import environ

from pkg_resources import get_distribution
from pytest import mark, raises
from typer import Exit, Option
from typer.testing import CliRunner

from falca.cli.base import Command
from falca.cli.inspect import inspect_command
from falca.exceptions import FalcaError

runner = CliRunner()


def test_add_command(cli: Command):
    def echo(msg: str = Option("hello world")):
        print(msg)

    cli.command("echo")(echo)
    result = runner.invoke(cli, ["echo", "--msg", "not found"])
    assert result.stdout == "not found\n"


def test_add_group(cli: Command):
    group = Command(name="group")

    @group.command("foo")
    def foo():
        print("bar")

    cli.add_typer(group)
    result = runner.invoke(cli, ["group", "foo"])
    assert result.stdout == "bar\n"


def test_merge_command(cli: Command):
    sub = Command(name="sub")

    @sub.command("runserver")
    def runserver():
        print("tertipu kau bgst")

    group = Command(name="group")

    @group.command("bar")
    def bar():
        print("foo")

    sub.add_typer(group)
    cli.merge(sub)
    result = runner.invoke(cli, ["runserver"])
    assert result.stdout == "tertipu kau bgst\n"
    result = runner.invoke(cli, ["group", "foo"])
    assert "No such command 'foo'" in result.stdout
    result = runner.invoke(cli, ["group", "bar"])
    assert result.stdout == "foo\n"


def test_invalid_app(capsys):
    environ.pop("FALCA_APP", None)
    with raises(Exit) as e:
        Command(name="test")

    log = capsys.readouterr()
    assert "can't find app" in log.out

    environ["FALCA_APP"] = "tests.conftest._fake_app"
    with raises(FalcaError) as e:
        Command(name="test")

    exc = e.value
    assert "Invalid application type" in exc.args[0]


def test_version(cli):
    result = runner.invoke(cli, ["--version"])
    version = get_distribution("falca").version
    assert f"Falca v{version}" in result.stdout


@mark.order(after="test_routers.py::test_conflict_router")
def test_inspect(wsgi_app):
    class Ctx:
        obj = wsgi_app

    ctx = Ctx()
    inspect_command(ctx)
