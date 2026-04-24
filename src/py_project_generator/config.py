"""Configuration settings for the generator."""

from pathlib import Path

CLI_CONTEXT_SETTINGS = {
    "help_option_names": ["-h", "--help"],
}

# Resolve the absolute path to the bundled cookiecutter template.
PACKAGE_DIR = Path(__file__).resolve().parent
TEMPLATES_ROOT = PACKAGE_DIR / "templates"

def get_template_dir(template_name: str) -> Path:
    """Return the path to a specific cookiecutter template."""
    template_dir = TEMPLATES_ROOT / f"cookiecutter-{template_name}"
    if not template_dir.exists():
        raise FileNotFoundError(f"Template '{template_name}' not found at {template_dir}")
    return template_dir
