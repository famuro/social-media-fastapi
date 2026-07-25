# Social Media API

A production-style social media backend API built with FastAPI and modern Python tooling.

This project is being developed incrementally to demonstrate backend engineering practices including API design, database integration, authentication, testing, containerization, and CI/CD workflows.

## Tech Stack

- Python
- FastAPI
- Pydantic Settings
- SQLModel
- PostgreSQL
- Alembic
- Docker
- Pytest
- Ruff
- GitHub Actions

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
- [ ] Database integration
- [ ] Database migrations
- [ ] Authentication
- [ ] Core social media features
- [ ] Testing
- [ ] Containerization
- [ ] CI/CD

## API

All API routes are versioned.

Current API version:

```
/api/v1
```

### Health Check

```
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
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── router.py
│   │       └── endpoints/
│   │           └── health.py
│   │
│   ├── core/
│   │   └── config.py
│   │
│   ├── schemas/
│   │   └── health.py
│   │
│   ├── main.py
│
├── tests/
├── .env.example
├── LICENSE
├── pyproject.toml
├── uv.lock
├── README.md
└── .gitignore
```

## Running the Application

Install dependencies:

```bash
uv sync
```

Run the development server:

```bash
uv run uvicorn app.main:app --reload
```

API documentation:

```
http://localhost:8000/docs
```

## License

This project is licensed under the MIT License.