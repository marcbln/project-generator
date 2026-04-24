"""Tests for the main CLI."""

from typer.testing import CliRunner

from py_project_generator.cli import app

runner = CliRunner()


def test_version() -> None:
    """Version command should return successfully."""
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "version" in result.stdout


def test_help() -> None:
    """Global help should be available via -h."""
    result = runner.invoke(app, ["-h"])
    assert result.exit_code == 0
    assert "Show this message and exit." in result.stdout
