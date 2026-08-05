"""Exceptions raised by authentication workflows."""


class InvalidTokenError(Exception):
    """Raised when an authentication token cannot be trusted."""

    def __init__(self, message: str = "Invalid authentication token.") -> None:
        """Initialize the invalid-token exception."""

        super().__init__(message)
