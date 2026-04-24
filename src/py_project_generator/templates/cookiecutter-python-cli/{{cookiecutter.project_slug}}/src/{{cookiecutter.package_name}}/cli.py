"""CLI entry point for {{ cookiecutter.project_name }}."""

import typer

app = typer.Typer(
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)


@app.command()
def main() -> None:
    """Run the default command."""
    typer.echo("Hello from {{ cookiecutter.project_name }}")


if __name__ == "__main__":
    app()
