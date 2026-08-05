"""Exceptions raised by authentication workflows."""


class InvalidCredentialsError(Exception):
    """Raised when supplied authentication credentials are invalid."""

    def __init__(self, message: str = "Invalid username or password.") -> None:
        """Initialize the invalid-credentials exception."""

        super().__init__(message)


class InvalidTokenError(Exception):
    """Raised when an authentication token cannot be trusted."""

    def __init__(self, message: str = "Invalid authentication token.") -> None:
        """Initialize the invalid-token exception."""

        super().__init__(message)
