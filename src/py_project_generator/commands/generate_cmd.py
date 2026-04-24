"""Generate project command."""

import typer
from rich.console import Console
from rich.panel import Panel

from ..core.generator import ProjectGenerator

console = Console()


def main(
    project_name: str | None = typer.Argument(
        None,
        help="The name of the project to generate (e.g., 'My Awesome CLI').",
    ),
    output_dir: str = typer.Option(
        ".",
        "--output-dir",
        "-o",
        help="Directory where the project will be created.",
    ),
    no_input: bool = typer.Option(
        False,
        "--no-input",
        help="Do not prompt for parameters and only use overrides.",
    ),
) -> None:
    """Generate a new Python project from the standardized template."""
    console.print(Panel.fit("Python Project Generator", style="bold green"))

    extra_context: dict[str, str] = {}
    if project_name:
        extra_context["project_name"] = project_name

    generator = ProjectGenerator(console=console)

    try:
        result_path = generator.generate(
            output_dir=output_dir,
            no_input=no_input,
            extra_context=extra_context if extra_context else None,
        )
        console.print(
            f"\n[bold green]Project successfully created at:[/bold green] {result_path}"
        )
        console.print("\n[bold cyan]Next Steps:[/bold cyan]")
        console.print(f"  cd {result_path}")
        console.print("  just setup")
    except Exception as exc:
        console.print(f"\n[bold red]Error generating project:[/bold red] {exc}")
        raise typer.Exit(1) from exc
