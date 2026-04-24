"""Handles invocation of Cookiecutter."""

from pathlib import Path
from cookiecutter.main import cookiecutter
from rich.console import Console

class ProjectGenerator:
    """Encapsulates project generation logic."""

    def __init__(self, console: Console) -> None:
        self.console = console

    def generate(
        self,
        template_dir: str | Path,
        output_dir: str,
        no_input: bool = False,
        extra_context: dict[str, str] | None = None,
    ) -> str:
        """Run the bundled template generation and return the created path."""
        template_path = Path(template_dir)
        if not template_path.exists():
            raise FileNotFoundError(f"Template directory not found at {template_path}")

        self.console.print(f"[dim]Using template from: {template_path}[/dim]")

        result_dir = cookiecutter(
            str(template_path),
            no_input=no_input,
            extra_context=extra_context or {},
            output_dir=output_dir,
        )
        return str(result_dir)
