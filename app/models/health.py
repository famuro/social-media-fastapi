from sqlmodel import SQLModel


class HealthResponse(SQLModel):
    """Response model for the health check endpoint."""

    status: str
    database: str
