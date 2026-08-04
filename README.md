# Social Media API

A production-style social media backend API built with FastAPI and modern Python tooling.

This project is being developed incrementally to showcase modern backend engineering practices including: REST API, asynchronous programming, database integration, authentication, containerization, automated testing, and CI/CD workflows.

## Tech Stack

### Current

- **Server:** Python 3.14, FastAPI, SQLModel
- **Database:** PostgreSQL, Alembic migrations
- **Infrastructure:** Docker, Docker Compose, GitHub Actions
- **Quality:** Ruff, Pytest, Pre-commit

### Planned

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
- [x] Database migrations
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
│   ├── models/
│   │   ├── base.py
│   │   ├── health.py
│   │   └── user.py
│   │
│   └── main.py
│
├── migrations/
│   ├── versions/
│   ├── env.py
│   ├── README
│   └── script.py.mako
│
├── tests/
│   ├── api/
│   │   └── v1/
│   │       └── test_health.py 
│   │
│   ├── models/
│   │   └── test_user.py
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
make env
```

Build and start the application:

```bash
make build-up
```

The API will be available at:

```text
http://localhost:8000
```

Interactive API documentation:

```text
http://localhost:8000/docs
```

## Database Migrations

Create a migration after changing the database models:

```bash
make migration message="describe the schema change"
```

Apply all pending migrations:

```bash
make migrate
```

Downgrade the most recent migration:

```bash
make downgrade
```

View the migration history:

```bash
make migration-history
```

View the current database revision:

```bash
make migration-current
```

The migration commands automatically load the project environment and use a host-accessible PostgreSQL connection.


## Continuous Integration

GitHub Actions automatically validates every push and pull request to `main` by running:

- Ruff linting
- Ruff formatting checks
- Pytest
- Docker image build validation

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
