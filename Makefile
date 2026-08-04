.PHONY: help env lint lint-fix format format-check quality install-hooks run test
.PHONY: build-up up down clean docker-logs
.PHONY: migration migrate downgrade migration-history migration-current

help:
	@echo "Available commands:"
	@echo "  make build-up 			Build Docker image and start Docker services"
	@echo "  make up       			Start Docker services (in detached mode)"
	@echo "  make down     			Remove Docker services and networks"
	@echo "  make clean     		Remove Docker services, networks, and volumes"
	@echo "  make docker-logs     	View Docker logs"
	@echo "  make env     			Copy the example environment file to a real .env file"
	@echo "  make format        	Format code with Ruff"
	@echo "  make format-check  	Check formatting without changes"
	@echo "  make install-hooks 	Install git pre-commit hooks"
	@echo "  make lint          	Run Ruff linting"
	@echo "  make lint-fix      	Run Ruff linting and automatically fix issues"
	@echo "  make quality       	Run all code quality checks"
	@echo "  make run       		Run the api server"
	@echo "  make test       		Run the test suite"


env:
	cp .env.example .env

# uv commands
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


# Docker commands
up:
	docker compose up -d

build-up:
	docker compose up --build

down:
	docker compose down

clean:
	docker compose down -v

docker-logs:
	docker compose logs -f


# Alembic commands
migration:
	uv run alembic revision --autogenerate -m "$(message)"

migrate:
	uv run alembic upgrade head

downgrade:
	uv run alembic downgrade -1

migration-history:
	uv run alembic history --verbose

migration-current:
	uv run alembic current
