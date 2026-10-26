"""Replay tests: real DigiKey responses recorded once with vcrpy, replayed offline in CI.

Re-record (needs both apps, see CONTRIBUTING.md)::

    uv run pytest tests/replay --record-mode=rewrite

Product data is recorded from production (public catalog data). Order data comes from the
sandbox, which only returns dummy orders. Secrets and tokens are scrubbed before saving.
"""

from __future__ import annotations

import json
import os
from typing import Any

import pytest

from digikey import DigikeyClient

REDACTED = "REDACTED"
KEEP_RESPONSE_HEADERS = {"content-type", "x-ratelimit-limit", "x-ratelimit-remaining"}


def scrub_request(request: Any) -> Any:
    if request.path.endswith("/oauth2/token"):
        request.body = REDACTED
    return request


def scrub_response(response: dict[str, Any]) -> dict[str, Any]:
    response["headers"] = {k: v for k, v in response["headers"].items() if k.lower() in KEEP_RESPONSE_HEADERS}
    body = response["body"].get("string", b"")
    try:
        data = json.loads(body)
    except ValueError:
        return response
    if isinstance(data, dict) and "access_token" in data:
        data.update({k: REDACTED for k in ("access_token", "refresh_token") if k in data})
        response["body"]["string"] = json.dumps(data).encode()
    return response


@pytest.fixture(scope="module")
def vcr_config() -> dict[str, Any]:
    return {
        "filter_headers": [("Authorization", REDACTED), ("X-DIGIKEY-Client-Id", REDACTED), ("User-Agent", None)],
        "before_record_request": scrub_request,
        "before_record_response": scrub_response,
        "decode_compressed_response": True,
        "match_on": ["method", "scheme", "host", "path", "query"],
    }


def _client(prefix: str, sandbox: bool) -> DigikeyClient:
    # Real credentials are only needed when recording; replay works with any value.
    return DigikeyClient(
        os.getenv(f"DIGIKEY_{prefix}_CLIENT_ID") or "replay-client-id",
        os.getenv(f"DIGIKEY_{prefix}_CLIENT_SECRET") or "replay-client-secret",
        sandbox=sandbox,
        locale_site="US",
        locale_currency="USD",
    )


@pytest.fixture
def prod() -> DigikeyClient:
    return _client("PROD", sandbox=False)


@pytest.fixture
def sandbox() -> DigikeyClient:
    return _client("SANDBOX", sandbox=True)
