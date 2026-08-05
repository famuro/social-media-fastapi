"""Utilities for creating and validating authentication tokens."""

from datetime import UTC, datetime, timedelta
from typing import Final
from uuid import UUID

import jwt
from jwt.exceptions import InvalidTokenError as PyJWTInvalidTokenError
from pydantic import ValidationError

from app.core.config import settings
from app.exceptions.auth_exceptions import InvalidTokenError
from app.models.auth import TokenPayload

ACCESS_TOKEN_TYPE: Final = "access"

_REQUIRED_CLAIMS: Final[list[str]] = [
    "sub",
    "type",
    "iat",
    "exp",
]


def create_access_token(subject: UUID, expires_delta: timedelta | None = None) -> str:
    """Create a signed access token for a user."""

    issued_at = datetime.now(UTC)
    expires_at = issued_at + (
        expires_delta
        if expires_delta is not None
        else timedelta(minutes=settings.access_token_expire_minutes)
    )

    claims = {
        "sub": str(subject),
        "type": ACCESS_TOKEN_TYPE,
        "iat": issued_at,
        "exp": expires_at,
    }

    return jwt.encode(
        claims,
        settings.jwt_secret_key.get_secret_value(),
        algorithm=settings.jwt_algorithm,
    )


def decode_access_token(token: str) -> TokenPayload:
    """Decode and validate a signed access token."""

    try:
        claims = jwt.decode(
            token,
            settings.jwt_secret_key.get_secret_value(),
            algorithms=[settings.jwt_algorithm],
            options={
                "require": _REQUIRED_CLAIMS,
            },
        )

        payload = TokenPayload(
            subject=claims["sub"],
            token_type=claims["type"],
        )
    except (KeyError, PyJWTInvalidTokenError, ValidationError) as error:
        raise InvalidTokenError() from error

    if payload.token_type != ACCESS_TOKEN_TYPE:
        raise InvalidTokenError()

    return payload
