from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class ClientError(Exception):
    """
    Base exception for client-layer failures.

    Client errors are infrastructure-level and must not depend on FastAPI.
    They are translated to HTTP errors at the API boundary.
    """

    message: str

    def __str__(self) -> str:
        return self.message


@dataclass(slots=True)
class UpstreamHTTPError(ClientError):
    """
    Raised when an upstream service returns a non-2xx HTTP response.
    """

    status_code: int
    response_text: str
    is_retryable: bool = False


@dataclass(slots=True)
class NetworkError(ClientError):
    """
    Raised on network/connectivity issues.
    """

    is_retryable: bool = True


@dataclass(slots=True)
class ResponseParseError(ClientError):
    """
    Raised when the response cannot be parsed as expected (e.g., invalid JSON).
    """

    response_text: Optional[str] = None


@dataclass(slots=True)
class UnexpectedClientError(ClientError):
    """
    Raised for unexpected exceptions.
    """

    original: Optional[Exception] = None
