"""Tests for authentication token utilities."""

from datetime import timedelta
from uuid import UUID, uuid4

import jwt
import pytest

from app.core.config import settings
from app.core.tokens import ACCESS_TOKEN_TYPE, create_access_token, decode_access_token
from app.exceptions.auth_exceptions import InvalidTokenError


def test_create_and_decode_access_token() -> None:
    """A generated access token should preserve the user identity."""

    user_id = uuid4()

    token = create_access_token(subject=user_id)
    payload = decode_access_token(token)

    assert payload.subject == user_id
    assert payload.token_type == ACCESS_TOKEN_TYPE


def test_access_token_contains_expected_claims() -> None:
    """An access token should contain identity and lifecycle claims."""

    user_id = uuid4()
    token = create_access_token(subject=user_id)

    claims = jwt.decode(
        token,
        settings.jwt_secret_key.get_secret_value(),
        algorithms=[settings.jwt_algorithm],
    )

    assert claims["sub"] == str(user_id)
    assert claims["type"] == ACCESS_TOKEN_TYPE
    assert "iat" in claims
    assert "exp" in claims


def test_decode_access_token_rejects_expired_token() -> None:
    """An expired access token should not be accepted."""

    token = create_access_token(subject=uuid4(), expires_delta=timedelta(seconds=-1))

    with pytest.raises(InvalidTokenError):
        decode_access_token(token)


def test_decode_access_token_rejects_modified_token() -> None:
    """A token with a modified signature should not be accepted."""

    token = create_access_token(subject=uuid4())
    replacement = "a" if token[-1] != "a" else "b"
    modified_token = f"{token[:-1]}{replacement}"

    with pytest.raises(InvalidTokenError):
        decode_access_token(modified_token)


def test_decode_access_token_rejects_invalid_subject() -> None:
    """An access token subject must contain a valid user UUID."""

    token = jwt.encode(
        {
            "sub": "not-a-uuid",
            "type": ACCESS_TOKEN_TYPE,
            "iat": 1,
            "exp": 4_102_444_800,
        },
        settings.jwt_secret_key.get_secret_value(),
        algorithm=settings.jwt_algorithm,
    )

    with pytest.raises(InvalidTokenError):
        decode_access_token(token)


def test_decode_access_token_rejects_wrong_token_type() -> None:
    """An access-token decoder should reject other token categories."""

    user_id = uuid4()

    token = jwt.encode(
        {
            "sub": str(user_id),
            "type": "refresh",
            "iat": 1,
            "exp": 4_102_444_800,
        },
        settings.jwt_secret_key.get_secret_value(),
        algorithm=settings.jwt_algorithm,
    )

    with pytest.raises(InvalidTokenError):
        decode_access_token(token)


@pytest.mark.parametrize(
    "missing_claim",
    [
        "sub",
        "type",
        "iat",
        "exp",
    ],
)
def test_decode_access_token_rejects_missing_required_claim(
    missing_claim: str,
) -> None:
    """Access tokens must contain every required claim."""

    claims = {
        "sub": str(uuid4()),
        "type": ACCESS_TOKEN_TYPE,
        "iat": 1,
        "exp": 4_102_444_800,
    }
    claims.pop(missing_claim)

    token = jwt.encode(
        claims,
        settings.jwt_secret_key.get_secret_value(),
        algorithm=settings.jwt_algorithm,
    )

    with pytest.raises(InvalidTokenError):
        decode_access_token(token)


def test_token_payload_subject_is_uuid() -> None:
    """Decoded token subjects should use the domain UUID type."""

    token = create_access_token(subject=uuid4())

    payload = decode_access_token(token)

    assert isinstance(payload.subject, UUID)
