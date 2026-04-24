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
	uv run pytest --ignore=src/py_project_generator/templates

# run tests with coverage
coverage:
	uv run pytest --ignore=src/py_project_generator/templates --cov=src

# lint the code using ruff and mypy
lint:
	uv run ruff check src tests
	uv run mypy src tests

# format the code using ruff
format:
	uv run ruff check --fix src tests
	uv run ruff format src tests
