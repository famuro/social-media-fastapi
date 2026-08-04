"""Tests for password security utilities."""

from app.core.security import hash_password, verify_password


def test_hash_password_does_not_return_plaintext() -> None:
    """Password hashes should not contain the original plaintext value."""

    password: str = "v3rYSTr0nGp@s$woRd"

    hashed_password = hash_password(password)

    assert hashed_password != password


def test_hash_password_generates_distinct_salted_hashes() -> None:
    """Hashing the same password twice should produce different hashes."""

    password: str = "v3rYSTr0nGp@s$woRd"

    first_hash = hash_password(password)
    second_hash = hash_password(password)

    assert first_hash != second_hash


def test_verify_password_accepts_matching_password() -> None:
    """Verification should succeed when plaintext matches the stored hash."""

    password: str = "v3rYSTr0nGp@s$woRd"
    hashed_password: str = hash_password(password)

    assert verify_password(password, hashed_password) is True


def test_verify_password_rejects_nonmatching_password() -> None:
    """Verification should fail when plaintext does not match the hash."""

    hashed_password: str = hash_password("correct-password")

    assert verify_password("incorrect-password", hashed_password) is False
