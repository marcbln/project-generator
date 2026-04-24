# Python Project Generator

A strict, cookiecutter-backed scaffolding tool that enforces Topdata Python conventions out of the box.

## Requirements

- Python 3.12+
- uv package manager
- just command runner

## Installation

```bash
git clone <repository>
cd py-project-generator
just setup
```

## Usage

### Command Structure

```bash
pypg generate <template-type> <project-name> [options]
```

### Available Templates

- **python-cli**: Scaffolds a Python CLI application
- **sw6-plugin**: Scaffolds a Shopware 6 plugin
- **sw6-theme**: Scaffolds a Shopware 6 theme

### Examples

Generate a Python CLI project (with prompts):

```bash
pypg generate python-cli "My Awesome Tool"
```

Generate a Python CLI project with custom output directory:

```bash
pypg generate python-cli "My Awesome Tool" -o ~/devel
```

Generate a Shopware 6 plugin (no interactive prompts):

```bash
pypg generate sw6-plugin TopdataMyNewPluginSW6 --no-input
```

Generate a SW6 plugin in a specific directory:

```bash
pypg generate sw6-plugin TopdataMyNewPluginSW6 -o /topdata/sw6-plugins --no-input
```

Generate a Shopware 6 theme:

```bash
pypg generate sw6-theme TopdataMyNewThemeSW6 --no-input
```

Generate a SW6 theme in a specific directory:

```bash
pypg generate sw6-theme TopdataMyNewThemeSW6 -o /topdata/sw6-themes --no-input
```

### Options

- `-o, --output-dir`: Directory where the project will be created (default: current directory)
- `--no-input`: Skip interactive prompts and use defaults/overrides only
