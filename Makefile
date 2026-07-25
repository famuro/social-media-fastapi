.PHONY: help lint lint-fix format format-check quality

help:
	@echo "Available commands:"
	@echo "  make lint          Run Ruff linting"
	@echo "  make lint-fix      Run Ruff linting and automatically fix issues"
	@echo "  make format        Format code with Ruff"
	@echo "  make format-check  Check formatting without changes"
	@echo "  make quality       Run all code quality checks"


lint:
	uv run ruff check .


lint-fix:
	uv run ruff check . --fix


format:
	uv run ruff format .


format-check:
	uv run ruff format --check .


quality:
	make lint
	make format-check
