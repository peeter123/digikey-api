"""Smoke tests against the real DigiKey API, run weekly by .github/workflows/live.yml.

They catch API changes the recorded cassettes cannot. Run locally with::

    DIGIKEY_LIVE=1 uv run pytest -m live
"""

from __future__ import annotations

import os

import pytest

from digikey import DigikeyClient

pytestmark = [
    pytest.mark.live,
    pytest.mark.skipif(os.getenv("DIGIKEY_LIVE") != "1", reason="set DIGIKEY_LIVE=1 to call the real API"),
]


def client(prefix: str, sandbox: bool) -> DigikeyClient:
    client_id = os.getenv(f"DIGIKEY_{prefix}_CLIENT_ID")
    client_secret = os.getenv(f"DIGIKEY_{prefix}_CLIENT_SECRET")
    if not client_id or not client_secret:
        pytest.skip(f"DIGIKEY_{prefix}_CLIENT_ID / _SECRET not set")
    return DigikeyClient(client_id, client_secret, sandbox=sandbox)


def test_production_product_search() -> None:
    prod = client("PROD", sandbox=False)
    found = prod.keyword_search("LM358")
    assert found.products
    details = prod.product_details("296-6501-1-ND")
    assert details.product is not None and details.product.manufacturer_product_number
    assert prod.rate_limit.remaining is None or prod.rate_limit.remaining >= 0


def test_sandbox_product_search() -> None:
    assert client("SANDBOX", sandbox=True).keyword_search("LM358").products is not None


def test_sandbox_order_history() -> None:
    assert client("SANDBOX", sandbox=True).search_orders(page_size=1) is not None
