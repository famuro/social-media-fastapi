# Social Media API

A production-style social media backend API built with FastAPI and modern Python tooling.

This project is being developed incrementally to showcase modern backend engineering practices including: REST API, asynchronous programming, database integration, authentication, containerization, automated testing, and CI/CD workflows.

## Tech Stack

### Current

- **Backend:** Python 3.14, FastAPI, PostgreSQL
- **Infrastructure:** Docker, Docker Compose, GitHub Actions
- **Quality:** Ruff, Pytest, Pre-commit

### Planned

- Alembic
- JWT Authentication

## Project Status

🚧 This project is actively under development.

Current progress:

- [x] Project initialization
- [x] FastAPI application setup
- [x] Application configuration
- [x] Versioned API structure
- [x] Database health check
- [x] Development tooling (Ruff, Makefile, pre-commit)
- [x] Continuous integration (GitHub Actions)
- [x] Testing infrastructure
- [x] Containerization 
- [x] PostgreSQL database integration
- [ ] Database migrations
- [ ] Authentication
- [ ] Core social media features

## API

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
  "status": "healthy",
  "database": "connected"
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
│   ├── db/
│   │   └── session.py
│   │
│   ├── schemas/
│   │   └── health.py
│   │
│   └── main.py
│
├── tests/
│   ├── api/
│   │   └── v1/
│   │       └── test_health.py 
│   │
│   └── conftest.py  
│
├── .dockerignore
├── .env.example
├── .gitignore
├── .pre-commit-config.yaml
├── docker-compose.yaml
├── Dockerfile
├── LICENSE
├── Makefile
├── pyproject.toml
├── README.md
└── uv.lock
```

### Getting Started

Create a local environment file:

```bash
cp .env.example .env
```

Build and start the application:

```bash
make build-up
```

The API will be be available at:

```text
http://localhost:8000
```

Interactive API documentation:

```text
http://localhost:8000/docs
```

## Continuous Integration

GitHub Actions automatically validates every push and pull request to `main` by running:

- Ruff linting
- Ruff formatting checks
- Pytest
- Docker image build validation

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
