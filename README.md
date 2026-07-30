# Social Media API

A production-style social media backend API built with FastAPI and modern Python tooling.

This project is being developed incrementally to demonstrate backend engineering practices including API design, database integration, authentication, testing, containerization, and CI/CD workflows.

## Tech Stack

### Current

- Python 3.14
- FastAPI
- Pydantic Settings
- Ruff
- pre-commit
- GitHub Actions
- Pytest
- Docker (Compose)

### Planned

- PostgreSQL
- SQLModel
- Alembic
- JWT Authentication

## Project Goals

The goal of this project is to build a realistic backend application while following modern backend engineering practices:

- Clean and maintainable application architecture
- Versioned REST API design
- Async API and database operations
- Database migrations
- Authentication and authorization
- Automated testing
- Containerized development
- Continuous integration and deployment

## Configuration

Application configuration is managed using environment variables through Pydantic Settings.

For local development, copy the example environment file:

```bash
cp .env.example .env
```

Environment-specific values are loaded at application startup and kept separate from source code.

## Current Status

🚧 This project is actively under development.

Current progress:

- [x] Project initialization
- [x] FastAPI application setup
- [x] Application configuration
- [x] Versioned API structure
- [x] Health check endpoint
- [x] Development tooling (Ruff, Makefile, pre-commit)
- [x] Continuous integration (GitHub Actions)
- [x] Testing infrastructure
- [ ] 🔄 Containerization 
- [ ] Database integration
- [ ] Database migrations
- [ ] Authentication
- [ ] Core social media features

## API

All API routes are versioned.

Current API version:

```text
/api/v1
```

### Health Check

```http
GET /api/v1/health
```

Example response:

```json
{
  "status": "healthy"
}
```

## Project Structure

```text
social-media-fastapi/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   └── health.py
│   │       └── router.py
│   │
│   ├── core/
│   │   └── config.py
│   │
│   ├── schemas/
│   │   └── health.py
│   │
│   └── main.py
│
├── tests/
├── .env.example
├── .pre-commit-config.yaml
├── Makefile
├── LICENSE
├── pyproject.toml
├── uv.lock
├── README.md
└── .gitignore
```

## Development

Install project dependencies:

```bash
uv sync
```

Install the Git pre-commit hooks:

```bash
make install-hooks
```

Common development commands:

```bash
make lint
make lint-fix
make format
make format-check
make install-hooks
make quality
make run
make test
```

Run the development server:

```bash
make run
```

Run with Docker:

```bash
make build-up
```

API documentation:

```text
http://localhost:8000/docs
```

## Continuous Integration

GitHub Actions automatically validates code quality for every pull request and every push to the `main` branch.

The workflow currently performs:

- Ruff linting
- Ruff formatting checks
- Pytest test suite

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
