"""Generate project command."""

import typer
from rich.console import Console
from rich.panel import Panel

from ..core.generator import ProjectGenerator
from ..config import get_template_dir
from ..utils.string_utils import StringUtils

console = Console()


def main(
    template_type: str = typer.Argument(
        ...,
        help="Type of project to generate (e.g., 'python-cli', 'sw6-plugin').",
    ),
    project_name: str = typer.Argument(
        ...,
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
    """Generate a new project from a standardized template."""
    console.print(Panel.fit(f"{template_type.title()} Generator", style="bold green"))

    target_template_dir = get_template_dir(template_type)

    extra_context: dict[str, str] = {}
    if project_name:
        extra_context["project_name"] = project_name
        
    if template_type == "sw6-plugin":
        if not project_name[0].isupper():
            raise typer.BadParameter("SW6 Plugin name must be PascalCase.")
        
        normalized = StringUtils.normalize_plugin_name(project_name)
        plugin_slug = StringUtils.to_dash_case(project_name)
        if plugin_slug.endswith("-sw6"):
            plugin_slug = plugin_slug[:-4]

        extra_context["plugin_name"] = project_name
        extra_context["plugin_name_normalized"] = normalized
        extra_context["plugin_name_with_hyphens"] = StringUtils.to_dash_case(project_name)
        extra_context["namespace"] = f"Topdata\\\\{project_name}"
        extra_context["composer_package_name"] = f"topdata/{plugin_slug}"

    if template_type == "sw6-theme":
        if not project_name[0].isupper():
            raise typer.BadParameter("SW6 Theme name must be PascalCase.")

        normalized = StringUtils.normalize_plugin_name(project_name)
        theme_slug = StringUtils.to_dash_case(project_name)
        if theme_slug.endswith("-sw6"):
            theme_slug = theme_slug[:-4]

        extra_context["theme_name"] = project_name
        extra_context["theme_name_normalized"] = normalized
        extra_context["theme_name_with_hyphens"] = StringUtils.to_dash_case(project_name)
        extra_context["theme_class"] = project_name
        extra_context["namespace"] = f"Topdata\\\\{project_name}"
        extra_context["composer_package_name"] = f"topdata/{theme_slug}"

    generator = ProjectGenerator(console=console)

    try:
        result_path = generator.generate(
            template_dir=target_template_dir,
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
