"""Security utilities for hashing and verifying passwords."""

from pwdlib import PasswordHash

_password_hasher: PasswordHash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Return a secure hash for a plaintext password."""

    return _password_hasher.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Return whether a plaintext password matches a stored hash."""

    return _password_hasher.verify(password, hashed_password)
