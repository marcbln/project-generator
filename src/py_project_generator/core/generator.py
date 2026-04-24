"""Handles invocation of Cookiecutter."""

from cookiecutter.main import cookiecutter
from rich.console import Console

from ..config import TEMPLATE_DIR


class ProjectGenerator:
    """Encapsulates project generation logic."""

    def __init__(self, console: Console) -> None:
        self.console = console

    def generate(
        self,
        output_dir: str,
        no_input: bool = False,
        extra_context: dict[str, str] | None = None,
    ) -> str:
        """Run the bundled template generation and return the created path."""
        if not TEMPLATE_DIR.exists():
            raise FileNotFoundError(f"Template directory not found at {TEMPLATE_DIR}")

        self.console.print(f"[dim]Using template from: {TEMPLATE_DIR}[/dim]")

        result_dir = cookiecutter(
            str(TEMPLATE_DIR),
            no_input=no_input,
            extra_context=extra_context or {},
            output_dir=output_dir,
        )
        return str(result_dir)
