"""CLI smoke tests."""

from importlib import import_module

from typer.testing import CliRunner

APP_MODULE = "{{ cookiecutter.package_name }}.cli"
app = import_module(APP_MODULE).app

runner = CliRunner()


def test_help() -> None:
    """Ensure help output is available via -h."""
    result = runner.invoke(app, ["-h"])
    assert result.exit_code == 0
    assert "Usage" in result.stdout
