.PHONY: help lint lint-fix format format-check quality install-hooks run test

help:
	@echo "Available commands:"
	@echo "  make format        Format code with Ruff"
	@echo "  make format-check  Check formatting without changes"
	@echo "  make install-hooks Install git pre-commit hooks"
	@echo "  make lint          Run Ruff linting"
	@echo "  make lint-fix      Run Ruff linting and automatically fix issues"
	@echo "  make quality       Run all code quality checks"
	@echo "  make run       	Run the api server"
	@echo "  make test       	Run the test suite"



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


install-hooks:
	uv run pre-commit install


run:
	uv run uvicorn app.main:app


test:
	uv run pytest
