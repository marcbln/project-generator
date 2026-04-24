"""Configuration settings for the generator."""

from pathlib import Path

CLI_CONTEXT_SETTINGS = {
    "help_option_names": ["-h", "--help"],
}

# Resolve the absolute path to the bundled cookiecutter template.
PACKAGE_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = PACKAGE_DIR / "templates" / "cookiecutter-python-cli"
