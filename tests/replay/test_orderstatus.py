from __future__ import annotations

import os
from pathlib import Path

import pytest

from digikey import DigikeyClient

CASSETTE = Path(__file__).parent / "cassettes" / "test_orderstatus" / "test_search_and_retrieve_orders.yaml"

pytestmark = [
    pytest.mark.vcr,
    # Recording needs a sandbox app subscribed to OrderStatus v4; until then the unit tests cover it.
    pytest.mark.skipif(
        not CASSETTE.exists() and not os.getenv("DIGIKEY_SANDBOX_CLIENT_ID"),
        reason="no OrderStatus cassette recorded yet",
    ),
]


def test_search_and_retrieve_orders(sandbox: DigikeyClient) -> None:
    orders = sandbox.search_orders(start_date="2024-01-01", end_date="2026-01-01", page_size=5)
    assert orders.orders, "the sandbox always returns example orders"
    sales_order_id = orders.orders[0].sales_orders[0].sales_order_id
    order = sandbox.retrieve_sales_order(sales_order_id)
    assert order.sales_order_id == sales_order_id
