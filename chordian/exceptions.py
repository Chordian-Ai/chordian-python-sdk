"""Exception hierarchy for the Chordian SDK.

Every error raised by the SDK is a subclass of :class:`ChordianError`, so callers
can catch the base class to handle any failure. HTTP failures are mapped to a
specific subclass based on the response status code (see :func:`raise_for_status`).
"""

from typing import Any, Optional


class ChordianError(Exception):
    """Base class for every error raised by the Chordian SDK."""

    def __init__(
        self,
        message: str,
        *,
        status_code: Optional[int] = None,
        error_type: Optional[str] = None,
        body: Any = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_type = error_type
        self.body = body

    def __str__(self) -> str:
        if self.status_code is not None:
            return f"[{self.status_code}] {self.message}"
        return self.message


class NoApiKeyError(ChordianError):
    """Raised when no API key has been configured.

    Set ``chordian.api_key = "..."`` or export the ``CHORDIAN_API_KEY``
    environment variable before making a request.
    """


class AuthenticationError(ChordianError):
    """Raised on ``401`` – the API key is missing, malformed or invalid."""


class PermissionDeniedError(ChordianError):
    """Raised on ``403`` – the API key is valid but not allowed to perform the action."""


class NotFoundError(ChordianError):
    """Raised on ``404`` – the requested resource does not exist."""


class ValidationError(ChordianError):
    """Raised on ``400`` / ``422`` – the request payload failed validation."""


class RateLimitError(ChordianError):
    """Raised on ``429`` – too many requests for the service ID."""


class ServerError(ChordianError):
    """Raised on ``5xx`` – Chordian encountered an internal error."""


class APITimeoutError(ChordianError):
    """Raised when a request exceeds the configured timeout.

    Long-running endpoints (e.g. ``CompanySearch.start``) can take a while to
    respond. Increase ``chordian.timeout`` (seconds), or set it to ``None`` to
    disable the timeout entirely.
    """


class APIConnectionError(ChordianError):
    """Raised when the SDK cannot reach the Chordian API (network/DNS/TLS)."""


class ApiError(ChordianError):
    """Raised for any other non-2xx response not covered above."""


# Mapping of HTTP status code -> exception class. ``raise_for_status`` falls back
# to ranges (4xx -> ApiError, 5xx -> ServerError) for codes not listed here.
_STATUS_MAP = {
    400: ValidationError,
    401: AuthenticationError,
    403: PermissionDeniedError,
    404: NotFoundError,
    422: ValidationError,
    429: RateLimitError,
}


def error_for_status(
    status_code: int, message: str, *, error_type: Optional[str] = None, body: Any = None
) -> ChordianError:
    """Return the appropriate :class:`ChordianError` subclass for ``status_code``."""
    cls = _STATUS_MAP.get(status_code)
    if cls is None:
        cls = ServerError if status_code >= 500 else ApiError
    return cls(message, status_code=status_code, error_type=error_type, body=body)
