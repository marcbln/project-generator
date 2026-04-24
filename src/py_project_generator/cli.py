"""Main CLI entry point."""

import typer
from rich.console import Console

from .commands import generate_cmd
from .config import CLI_CONTEXT_SETTINGS

console = Console()

app = typer.Typer(
    context_settings=CLI_CONTEXT_SETTINGS,
    no_args_is_help=True,
    help="Python Project Generator - Scaffolds modern Python CLIs.",
)


@app.command()
def version() -> None:
    """Show the application version."""
    from . import __version__

    console.print(
        f"[cyan]py-project-generator[/cyan] version [green]{__version__}[/green]"
    )


app.command(name="generate")(generate_cmd.main)


def main() -> None:
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
