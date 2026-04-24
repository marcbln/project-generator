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

Run the generation wizard:

```bash
uv run py-project-generator generate
```

Or pass variables explicitly:

```bash
uv run py-project-generator generate "My Super Tool" -o ./projects
```
