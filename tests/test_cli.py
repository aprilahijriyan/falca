from typer import Option
from typer.testing import CliRunner

from falca.cli.base import Command

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
