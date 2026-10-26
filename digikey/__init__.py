"""Python client for the DigiKey v4 APIs.

Use :class:`DigikeyClient` for new code. The module-level functions are kept for scripts written
for digikey-api 1.x; they use a client configured from the ``DIGIKEY_*`` environment variables.
"""

from __future__ import annotations

import os
from importlib.metadata import PackageNotFoundError, version
from typing import Any

from digikey.client import DigikeyClient, RateLimit
from digikey.exceptions import (
    DigikeyApiError,
    DigikeyAuthError,
    DigikeyError,
    DigikeyOauthException,
    DigikeyRateLimitError,
)
from digikey.oauth import AuthorizationCodeAuth, ClientCredentialsAuth, TokenProvider
from digikey.v4 import orderstatus, productsearch

try:
    __version__ = version("digikey-api")
except PackageNotFoundError:  # pragma: no cover - running from a source tree without metadata
    __version__ = "0+unknown"

__all__ = [
    "AuthorizationCodeAuth",
    "ClientCredentialsAuth",
    "DigikeyApiError",
    "DigikeyAuthError",
    "DigikeyClient",
    "DigikeyError",
    "DigikeyOauthException",
    "DigikeyRateLimitError",
    "RateLimit",
    "TokenProvider",
    "default_client",
    "digi_reel_pricing",
    "keyword_search",
    "product_details",
    "salesorder_history",
    "status_salesorder_id",
]

_ENV = (
    "DIGIKEY_CLIENT_ID",
    "DIGIKEY_CLIENT_SECRET",
    "DIGIKEY_CLIENT_SANDBOX",
    "DIGIKEY_AUTH_FLOW",
    "DIGIKEY_STORAGE_PATH",
    "DIGIKEY_LOCALE_SITE",
    "DIGIKEY_LOCALE_LANGUAGE",
    "DIGIKEY_LOCALE_CURRENCY",
    "DIGIKEY_ACCOUNT_ID",
)
_default: tuple[tuple[str | None, ...], DigikeyClient] | None = None


def default_client() -> DigikeyClient:
    """The client used by the module-level functions, rebuilt when the environment changes."""
    global _default
    key = tuple(os.getenv(name) for name in _ENV)
    if _default is None or _default[0] != key:
        _default = (key, DigikeyClient.from_env())
    return _default[1]


def keyword_search(
    request: productsearch.KeywordRequest | str | None = None, *, body: Any = None, **params: Any
) -> productsearch.KeywordResponse:
    """See :meth:`DigikeyClient.keyword_search`. ``body=`` is accepted as in 1.x."""
    request = request if request is not None else body
    if request is None:
        raise DigikeyError("keyword_search needs a KeywordRequest or a keyword")
    return default_client().keyword_search(request, **params)


def product_details(product_number: str, **params: Any) -> productsearch.ProductDetails:
    """See :meth:`DigikeyClient.product_details`."""
    return default_client().product_details(product_number, **params)


def digi_reel_pricing(product_number: str, requested_quantity: int, **params: Any) -> productsearch.DigiReelPricing:
    """See :meth:`DigikeyClient.digi_reel_pricing`."""
    return default_client().digi_reel_pricing(product_number, requested_quantity, **params)


def status_salesorder_id(sales_order_id: int, **params: Any) -> orderstatus.SalesOrder:
    """1.x name for :meth:`DigikeyClient.retrieve_sales_order`."""
    return default_client().retrieve_sales_order(sales_order_id, **params)


def salesorder_history(**params: Any) -> orderstatus.OrderResponse:
    """1.x name for :meth:`DigikeyClient.search_orders` (``start_date``/``end_date`` as before)."""
    return default_client().search_orders(**params)
