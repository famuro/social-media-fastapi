"""Exceptions raised by user workflows."""


class UserAlreadyExistsError(Exception):
    """Raised when a user conflicts with an existing unique field."""

    def __init__(self, field: str | None = None) -> None:
        """Initialize the exception with the conflicting field, when known."""

        self.field = field

        if field is None:
            message = "A user with the supplied details already exists."
        else:
            message = f"A user with that {field} already exists."

        super().__init__(message)
