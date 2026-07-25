# Social Media API

A production-style social media backend API built with FastAPI and modern Python tooling.

This project is being developed incrementally to demonstrate backend engineering practices including API design, database integration, testing, containerization, and CI/CD workflows.

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLModel
- Alembic
- Docker
- Pytest
- Ruff
- GitHub Actions

## Configuration

Application configuration is managed using environment variables through Pydantic Settings.

For local development, copy the example environment file:

```bash
cp .env.example .env
````

## Project Goals

The goal of this project is to build a realistic backend application while following industry best practices:

- Clean and maintainable application architecture
- Async API and database operations
- Database migrations
- Authentication and authorization
- Automated testing
- Containerized development
- Continuous integration and deployment

## Current Status

🚧 This project is actively under development.

Current progress:

- [x] Project initialization
- [x] FastAPI application setup
- [ ] Application configuration
- [ ] Health check endpoint
- [ ] Database integration
- [ ] Authentication
- [ ] Core social media features
- [ ] Testing
- [ ] Containerization
- [ ] CI/CD

## Project Structure

```text
social-media-api/
├── app/
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   │
│   ├── __init__.py
│   └── main.py
│
├── tests/
├── .env.example
├── pyproject.toml
├── uv.lock
├── README.md
└── .gitignore
```

## API

### Health Check

The API currently provides a basic root endpoint:
```text
GET /
```

Example response:

```json
{
  "message": "Hello world from the Social Media API"
}
```

## License

This project is licensed under the MIT License.