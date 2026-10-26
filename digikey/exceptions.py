from __future__ import annotations

from collections.abc import Mapping
from typing import Any


class DigikeyError(Exception):
    """Base class for every error raised by this library."""


class DigikeyAuthError(DigikeyError):
    """Obtaining or refreshing an OAuth2 token failed, or the API rejected the token."""


class DigikeyApiError(DigikeyError):
    """The DigiKey API answered with an error status.

    ``detail`` is the human readable message DigiKey returned (``DKProblemDetails.detail``)
    when the body could be parsed, ``body`` is the raw response body.
    """

    def __init__(
        self,
        status: int,
        detail: str,
        *,
        body: str | None = None,
        headers: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(f"DigiKey API returned {status}: {detail}")
        self.status = status
        self.detail = detail
        self.body = body
        self.headers = dict(headers or {})


class DigikeyRateLimitError(DigikeyApiError):
    """The rate limit was exceeded (HTTP 429). ``retry_after`` is in seconds, when DigiKey sent it."""

    def __init__(self, *args: Any, retry_after: int | None = None, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.retry_after = retry_after


# Name used by digikey-api 1.x.
DigikeyOauthException = DigikeyAuthError
