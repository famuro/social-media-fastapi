"""Models used by authentication workflows."""

from uuid import UUID

from pydantic import BaseModel, ConfigDict


class Token(BaseModel):
    """Bearer token returned after successful authentication."""

    access_token: str
    token_type: str = "bearer"

    model_config = ConfigDict(extra="forbid")


class TokenPayload(BaseModel):
    """Validated claims extracted from an access token."""

    subject: UUID
    token_type: str

    model_config = ConfigDict(extra="forbid")
