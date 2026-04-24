---
filename: "_ai/backlog/archive/260424_2345__IMPLEMENTATION_PLAN__create-py-project-generator.md"
title: "Create Python Project Generator CLI"
createdAt: 2026-04-24 23:45
updatedAt: 2026-04-25 00:05
status: completed
priority: high
tags:[cli, cookiecutter, python, templating]
estimatedComplexity: moderate
documentType: IMPLEMENTATION_PLAN
---

## 1. Problem Statement
Setting up new Python CLI applications currently involves repetitive boilerplate work to ensure compliance with the company's coding conventions (Typer, Rich, UV, Just, Ruff, MyPy, Pytest). This manual process is time-consuming and prone to human error or configuration drift. A robust generation tool, similar to the existing `sw6-plugin-generator`, is needed to automate the scaffolding of new Python projects using Cookiecutter templates.

## 2. Executive Summary
This implementation plan outlines the development of `py-project-generator`, a Python CLI tool built with Typer. The tool bundles a pre-configured Cookiecutter template that enforces the strict Python conventions requested (including `justfile`, `uv` usage, `-h` help shortcuts, and proper directory structures). The generator will expose a user-friendly CLI to dynamically scaffold projects by either prompting for input or accepting command-line arguments.

## 3. Project Environment Details
```text
Python Version: 3.12+
Dependency Manager: uv
Task Runner: just
Libraries: typer, rich, cookiecutter, pytest, ruff, mypy
Structure: src/ package layout
Formatting/Linting: ruff
Type Checking: mypy
```

---

## Phase 1: Project Setup & Core Configuration

This phase establishes the root configuration for the generator tool itself, applying the exact conventions it aims to generate.

### `pyproject.toml` [NEW FILE]
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "py-project-generator"
version = "0.1.0"
description = "A generator for creating Python CLI projects using Cookiecutter and UV."
requires-python = ">=3.12"
authors = [
    { name = "Topdata GmbH", email = "info@topdata.de" }
]
dependencies = [
    "typer>=0.9.0",
    "rich>=13.7.0",
    "cookiecutter>=2.5.0",
    "pyyaml>=6.0",
]

[project.scripts]
py-project-generator = "py_project_generator.cli:main"

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=4.1.0",
    "mypy>=1.8.0",
    "ruff>=0.3.0",
]

[tool.ruff]
line-length = 88
lint.select = ["E", "F", "W", "I"]

[tool.mypy]
strict = true
```

### `justfile` [NEW FILE]
```justfile
set python-venv-path := ".venv"

# default task: list all commands
default: help

# show available tasks
help:
	@just --list

# setup the project using uv
setup:
	uv venv
	uv pip install -e ".[dev]"

# run tests
test:
	uv run pytest

# run tests with coverage
coverage:
	uv run pytest --cov=src

# lint the code using ruff and mypy
lint:
	uv run ruff check src tests
	uv run mypy src tests

# format the code using ruff
format:
	uv run ruff check --fix src tests
	uv run ruff format src tests
```

### `.gitignore` [NEW FILE]
```text
.venv/
.env
__pycache__/
*.py[cod]
*$py.class
.pytest_cache/
.ruff_cache/
.mypy_cache/
.idea/
.vscode/
```

---

## Phase 2: Bundling the Cookiecutter Template

We embed the Cookiecutter template directly within the generator package so it ships cleanly.

### `src/py_project_generator/templates/cookiecutter-python-cli/cookiecutter.json` [NEW FILE]
```json
{
    "project_name": "My Awesome CLI",
    "project_slug": "{{ cookiecutter.project_name.lower().replace(' ', '-') }}",
    "package_name": "{{ cookiecutter.project_slug.replace('-', '_') }}",
    "version": "0.1.0",
    "description": "A modern Python CLI application.",
    "author_name": "Topdata GmbH",
    "author_email": "info@topdata.de",
    "python_version": "3.12"
}
```

### `src/py_project_generator/templates/cookiecutter-python-cli/{{cookiecutter.project_slug}}/pyproject.toml` [NEW FILE]
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "{{ cookiecutter.project_slug }}"
version = "{{ cookiecutter.version }}"
description = "{{ cookiecutter.description }}"
requires-python = ">={{ cookiecutter.python_version }}"
authors = [
    { name = "{{ cookiecutter.author_name }}", email = "{{ cookiecutter.author_email }}" },
]
dependencies = [
    "typer>=0.9.0",
    "rich>=13.7.0",
    "pyyaml>=6.0",
    "python-dotenv>=1.0.0",
]

[project.scripts]
{{ cookiecutter.project_slug }} = "{{ cookiecutter.package_name }}.cli:main"

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=4.1.0",
    "mypy>=1.8.0",
    "ruff>=0.3.0",
]

[tool.ruff]
line-length = 88
lint.select = ["E", "F", "W", "I"]

[tool.mypy]
strict = true
```

### `src/py_project_generator/templates/cookiecutter-python-cli/{{cookiecutter.project_slug}}/justfile` [NEW FILE]
```justfile
set python-venv-path := ".venv"

default: help

help:
	@just --list

setup:
	uv venv
	uv pip install -e ".[dev]"

test:
	uv run pytest

coverage:
	uv run pytest --cov=src

lint:
	uv run ruff check src tests
	uv run mypy src tests

format:
	uv run ruff check --fix src tests
	uv run ruff format src tests

run +args="--help":
	uv run {{ cookiecutter.project_slug }} {{ "{{args}}" }}
```

---

## Phase 3: Core Business Logic (SOLID)

### `src/py_project_generator/__init__.py` [NEW FILE]
```python
"""Py Project Generator."""

__version__ = "0.1.0"
```

### `src/py_project_generator/config.py` [NEW FILE]
```python
"""Configuration settings for the generator."""

from pathlib import Path

CLI_CONTEXT_SETTINGS = {
    "help_option_names": ["-h", "--help"],
}

# Resolve the absolute path to the bundled cookiecutter template
PACKAGE_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = PACKAGE_DIR / "templates" / "cookiecutter-python-cli"
```

### `src/py_project_generator/core/__init__.py` [NEW FILE]
```python
"""Core business logic for generating projects."""
```

### `src/py_project_generator/core/generator.py` [NEW FILE]
```python
"""Handles the invocation of Cookiecutter."""

from cookiecutter.main import cookiecutter
from rich.console import Console

from ..config import TEMPLATE_DIR


class ProjectGenerator:
    """Encapsulates project generation logic (Single Responsibility)."""

    def __init__(self, console: Console):
        self.console = console

    def generate(self, output_dir: str, no_input: bool = False, extra_context: dict[str, str] | None = None) -> str:
        """Runs the cookiecutter template generation."""
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
```

---

## Phase 4: CLI Interface Implementation

### `src/py_project_generator/commands/__init__.py` [NEW FILE]
```python
"""CLI command modules."""
```

### `src/py_project_generator/commands/generate_cmd.py` [NEW FILE]
```python
"""Generate project command."""

import typer
from rich.console import Console
from rich.panel import Panel

from ..core.generator import ProjectGenerator

console = Console()


def main(
    project_name: str = typer.Argument(
        None, help="The name of the project to generate (e.g., 'My Awesome CLI')."
    ),
    output_dir: str = typer.Option(
        ".", "--output-dir", "-o", help="Directory where the project will be created."
    ),
    no_input: bool = typer.Option(
        False, "--no-input", help="Do not prompt for parameters and only use overrides."
    ),
) -> None:
    """Generate a new Python project from the standardized template."""
    console.print(Panel.fit("Python Project Generator", style="bold green"))

    extra_context = {}
    if project_name:
        extra_context["project_name"] = project_name

    generator = ProjectGenerator(console=console)

    try:
        result_path = generator.generate(
            output_dir=output_dir,
            no_input=no_input,
            extra_context=extra_context if extra_context else None
        )
        console.print(f"\n[bold green]✓ Project successfully created at:[/bold green] {result_path}")
        console.print("\n[bold cyan]Next Steps:[/bold cyan]")
        console.print(f"  cd {result_path}")
        console.print("  just setup")
    except Exception as e:
        console.print(f"\n[bold red]Error generating project:[/bold red] {e}")
        raise typer.Exit(1)
```

### `src/py_project_generator/cli.py` [NEW FILE]
```python
"""Main CLI entry point."""

import typer
from rich.console import Console

from .config import CLI_CONTEXT_SETTINGS
from .commands import generate_cmd

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
    console.print(f"[cyan]py-project-generator[/cyan] version [green]{__version__}[/green]")


app.command(name="generate")(generate_cmd.main)


def main() -> None:
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
```

---

## Phase 5: Automated Testing

### `tests/test_cli.py` [NEW FILE]
```python
"""Tests for the main CLI."""

from typer.testing import CliRunner
from py_project_generator.cli import app

runner = CliRunner()


def test_version() -> None:
    """Test the version command."""
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "version" in result.stdout


def test_help() -> None:
    """Test that -h shows help."""
    result = runner.invoke(app, ["-h"])
    assert result.exit_code == 0
    assert "Show this message and exit." in result.stdout
```

---

## Phase 6: Documentation

### `README.md` [NEW FILE]
```markdown
# Python Project Generator

A strict, cookiecutter-backed scaffolding tool that enforces Topdata Python conventions out of the box.

## Requirements
- Python 3.12+
- `uv` package manager
- `just` command runner

## Installation

```bash
git clone <repository>
cd py-project-generator
just setup
```

## Usage

Run the generation wizard:
```bash
uv run py-project-generator generate
```

Or pass variables explicitly:
```bash
uv run py-project-generator generate "My Super Tool" -o ./projects
```
```

---

## Phase 7: Implementation Report

Write an execution report based on this exact structure when the implementation is completed.

### `_ai/backlog/reports/{YYMMDD_HHmm}__IMPLEMENTATION_REPORT__create-py-project-generator.md` [NEW FILE]
```yaml
---
filename: "_ai/backlog/reports/{YYMMDD_HHmm}__IMPLEMENTATION_REPORT__create-py-project-generator.md"
title: "Report: Create Python Project Generator CLI"
createdAt: YYYY-MM-DD HH:mm
updatedAt: YYYY-MM-DD HH:mm
planFile: "_ai/backlog/active/260424_2345__IMPLEMENTATION_PLAN__create-py-project-generator.md"
project: "py-project-generator"
status: completed
filesCreated: 12
filesModified: 0
filesDeleted: 0
tags: [cli, cookiecutter, python, templating]
documentType: IMPLEMENTATION_REPORT
---
```

#### Report Content
1. **Summary**: Developed the `py-project-generator` using Typer. It dynamically utilizes Cookiecutter to instantiate fully configured, convention-adhering Python CLI applications.
2. **Files Changed**:
   - `pyproject.toml`, `justfile`, `.gitignore`: Setup for the generator.
   - `src/py_project_generator/templates/...`: Embedded cookiecutter templates.
   - `src/py_project_generator/cli.py` & `commands/generate_cmd.py`: Typer CLI and routing.
   - `src/py_project_generator/core/generator.py`: SOLID abstraction of cookiecutter execution.
3. **Key Changes**:
   - Applied Typer settings to show help natively (`no_args_is_help=True`) and support `-h`.
   - Templated `justfile` logic for downstream tasks.
4. **Technical Decisions**:
   - Included Cookiecutter programmatically via the Python API (`cookiecutter()`) rather than via a shell subprocess to allow clean context handling and error trapping.
5. **Testing Notes**: Run `just test` to verify CLI command bindings.
6. **Usage Examples**:
   - `uv run py-project-generator generate` (interactive)
   - `uv run py-project-generator generate "Data Importer" --no-input` (automated)
7. **Documentation Updates**: Provided `README.md` explaining bootstrapping setup.
8. **Next Steps**: Consider adding a configuration file loader to dynamically override default company configurations (e.g. `~/.config/topdata/project-defaults.yml`).
