from __future__ import annotations

import inspect
import json
import logging
import os
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from functools import cache
from typing import Any, Literal, Protocol, TypeVar

import urllib3

from digikey.exceptions import DigikeyApiError, DigikeyAuthError, DigikeyError, DigikeyRateLimitError
from digikey.oauth.oauth2 import PROD_HOST, SANDBOX_HOST, AuthorizationCodeAuth, ClientCredentialsAuth, TokenProvider
from digikey.v4 import orderstatus, productsearch

logger = logging.getLogger(__name__)

T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)


class _ApiResponse(Protocol[T_co]):
    """What the generated ``*_with_http_info`` methods return."""

    @property
    def data(self) -> T_co: ...

    @property
    def headers(self) -> Mapping[str, str] | None: ...


AuthFlow = Literal["client_credentials", "authorization_code", "authorization_code_manual"]

# Header parameters the generated methods take; filled in from the client settings.
_HEADER_PARAMS = (
    "x_digikey_client_id",
    "x_digikey_locale_site",
    "x_digikey_locale_language",
    "x_digikey_locale_currency",
    "x_digikey_account_id",
)


@dataclass(frozen=True)
class RateLimit:
    """Rate limit state reported by the last response, ``None`` when DigiKey did not send it."""

    limit: int | None = None
    remaining: int | None = None

    @classmethod
    def from_headers(cls, headers: Mapping[str, str] | None) -> RateLimit:
        headers = {k.lower(): v for k, v in (headers or {}).items()}
        return cls(_int(headers.get("x-ratelimit-limit")), _int(headers.get("x-ratelimit-remaining")))


class DigikeyClient:
    """Client for the DigiKey v4 ProductSearch and OrderStatus APIs.

    Methods return the generated pydantic models from :mod:`digikey.v4.productsearch` and
    :mod:`digikey.v4.orderstatus`. Optional query parameters are passed as keyword arguments with
    the names of the generated API methods, e.g. ``client.product_pricing("P5555-ND", in_stock=True)``.
    Errors raise :class:`~digikey.exceptions.DigikeyApiError` and friends.

    ``auth`` selects the OAuth2 flow: ``"client_credentials"`` (2-legged, default),
    ``"authorization_code"`` (3-legged, opens a browser once), ``"authorization_code_manual"``
    (3-legged, paste the redirect URL, for headless machines) or any :class:`TokenProvider`.
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        *,
        sandbox: bool = False,
        auth: AuthFlow | TokenProvider = "client_credentials",
        storage_path: str | os.PathLike[str] | None = None,
        locale_site: str | None = None,
        locale_language: str | None = None,
        locale_currency: str | None = None,
        account_id: str | None = None,
        timeout: float = 30,
    ) -> None:
        self.client_id = client_id
        self.sandbox = sandbox
        self.timeout = timeout
        self.auth = _make_auth(auth, client_id, client_secret, sandbox, storage_path)
        self.rate_limit = RateLimit()
        self._headers = {
            "x_digikey_client_id": client_id,
            "x_digikey_locale_site": locale_site,
            "x_digikey_locale_language": locale_language,
            "x_digikey_locale_currency": locale_currency,
            "x_digikey_account_id": account_id,
        }
        host = SANDBOX_HOST if sandbox else PROD_HOST
        self.product_search_api = productsearch.ProductSearchApi(
            _api_client(productsearch, f"{host}/products/v4", client_id)
        )
        self.order_history_api = orderstatus.OrderHistoryApi(
            _api_client(orderstatus, f"{host}/orderstatus/v4", client_id)
        )

    @classmethod
    def from_env(cls, **overrides: Any) -> DigikeyClient:
        """Build a client from the ``DIGIKEY_*`` environment variables (see README)."""
        client_id = os.getenv("DIGIKEY_CLIENT_ID")
        client_secret = os.getenv("DIGIKEY_CLIENT_SECRET")
        if not client_id or not client_secret:
            raise DigikeyError("Set DIGIKEY_CLIENT_ID and DIGIKEY_CLIENT_SECRET, or create a DigikeyClient directly")
        settings: dict[str, Any] = {
            "sandbox": _env_bool("DIGIKEY_CLIENT_SANDBOX"),
            "auth": os.getenv("DIGIKEY_AUTH_FLOW") or "client_credentials",
            "storage_path": os.getenv("DIGIKEY_STORAGE_PATH") or None,
            "locale_site": os.getenv("DIGIKEY_LOCALE_SITE") or None,
            "locale_language": os.getenv("DIGIKEY_LOCALE_LANGUAGE") or None,
            "locale_currency": os.getenv("DIGIKEY_LOCALE_CURRENCY") or None,
            "account_id": os.getenv("DIGIKEY_ACCOUNT_ID") or None,
        }
        return cls(client_id, client_secret, **{**settings, **overrides})

    # ProductSearch

    def keyword_search(
        self, request: productsearch.KeywordRequest | str, **params: Any
    ) -> productsearch.KeywordResponse:
        """Search products by keyword, part number or description. ``request`` may be a plain keyword."""
        if isinstance(request, str):
            request = productsearch.KeywordRequest(Keywords=request)
        return self._call(self.product_search_api.keyword_search_with_http_info, body=request, **params)

    def product_details(self, product_number: str, **params: Any) -> productsearch.ProductDetails:
        """Full product information, including pricing, for a DigiKey or manufacturer part number."""
        return self._call(
            self.product_search_api.product_details_with_http_info, product_number=product_number, **params
        )

    def product_pricing(self, product_number: str, **params: Any) -> productsearch.ProductPricingResponse:
        return self._call(
            self.product_search_api.product_pricing_with_http_info, product_number=product_number, **params
        )

    def pricing_options_by_quantity(
        self, product_number: str, requested_quantity: int, **params: Any
    ) -> productsearch.PricingOptionsForQuantityResponse:
        return self._call(
            self.product_search_api.pricing_options_by_quantity_with_http_info,
            product_number=product_number,
            requested_quantity=requested_quantity,
            **params,
        )

    def digi_reel_pricing(
        self, product_number: str, requested_quantity: int, **params: Any
    ) -> productsearch.DigiReelPricing:
        return self._call(
            self.product_search_api.digi_reel_pricing_with_http_info,
            product_number=product_number,
            requested_quantity=requested_quantity,
            **params,
        )

    def substitutions(self, product_number: str, **params: Any) -> productsearch.ProductSubstitutesResponse:
        return self._call(self.product_search_api.substitutions_with_http_info, product_number=product_number, **params)

    def recommended_products(self, product_number: str, **params: Any) -> productsearch.RecommendedProductsResponse:
        return self._call(
            self.product_search_api.recommended_products_with_http_info, product_number=product_number, **params
        )

    def associations(self, product_number: str, **params: Any) -> productsearch.ProductAssociationsResponse:
        return self._call(self.product_search_api.associations_with_http_info, product_number=product_number, **params)

    def alternate_packaging(self, product_number: str, **params: Any) -> productsearch.AlternatePackagingResponse:
        return self._call(
            self.product_search_api.alternate_packaging_with_http_info, product_number=product_number, **params
        )

    def media(self, product_number: str, **params: Any) -> productsearch.MediaResponse:
        return self._call(self.product_search_api.media_with_http_info, product_number=product_number, **params)

    def manufacturers(self, **params: Any) -> productsearch.ManufacturersResponse:
        return self._call(self.product_search_api.manufacturers_with_http_info, **params)

    def categories(self, **params: Any) -> productsearch.CategoriesResponse:
        return self._call(self.product_search_api.categories_with_http_info, **params)

    def categories_by_id(self, category_id: int, **params: Any) -> productsearch.CategoryResponse:
        return self._call(self.product_search_api.categories_by_id_with_http_info, category_id=category_id, **params)

    # OrderStatus

    def search_orders(self, **params: Any) -> orderstatus.OrderResponse:
        """Order history; filter with ``start_date``, ``end_date``, ``page_number``, ``page_size``, ``shared``."""
        return self._call(self.order_history_api.search_orders_with_http_info, **params)

    def retrieve_sales_order(self, sales_order_id: int, **params: Any) -> orderstatus.SalesOrder:
        return self._call(
            self.order_history_api.retrieve_sales_order_with_http_info, sales_order_id=sales_order_id, **params
        )

    def _call(self, method: Callable[..., _ApiResponse[T]], **params: Any) -> T:
        accepted = _parameters(method.__func__)  # type: ignore[attr-defined]
        for name in _HEADER_PARAMS:
            if name in accepted and self._headers[name] is not None:
                params.setdefault(name, self._headers[name])
        params.setdefault("_request_timeout", self.timeout)
        api_client = method.__self__.api_client  # type: ignore[attr-defined]

        for attempt in (1, 2):
            api_client.configuration.access_token = self.auth.access_token()
            try:
                response = method(**params)
            except (productsearch.ApiException, orderstatus.ApiException) as e:
                if e.status == 401 and attempt == 1:
                    logger.debug("Access token rejected, retrying with a new one")
                    self.auth.invalidate()
                    continue
                raise _api_error(e) from e
            except urllib3.exceptions.HTTPError as e:
                raise DigikeyError(f"Cannot reach the DigiKey API: {e}") from e
            self.rate_limit = RateLimit.from_headers(response.headers)
            return response.data
        raise AssertionError("unreachable")  # pragma: no cover


def _make_auth(
    auth: AuthFlow | TokenProvider,
    client_id: str,
    client_secret: str,
    sandbox: bool,
    storage_path: str | os.PathLike[str] | None,
) -> TokenProvider:
    if not isinstance(auth, str):
        return auth
    if auth == "client_credentials":
        return ClientCredentialsAuth(client_id, client_secret, sandbox=sandbox)
    if auth in ("authorization_code", "authorization_code_manual"):
        return AuthorizationCodeAuth(
            client_id,
            client_secret,
            sandbox=sandbox,
            storage_path=storage_path,
            manual=auth == "authorization_code_manual",
        )
    raise DigikeyAuthError(
        f"Unknown auth flow {auth!r}, use client_credentials, authorization_code or authorization_code_manual"
    )


def _api_client(package: Any, host: str, client_id: str) -> Any:
    from digikey import __version__

    configuration = package.Configuration(host=host, api_key={"apiKeySecurity": client_id})
    api_client = package.ApiClient(configuration)
    api_client.user_agent = f"digikey-api/{__version__} (+https://github.com/peeter123/digikey-api)"
    return api_client


@cache
def _parameters(method: Callable[..., Any]) -> frozenset[str]:
    return frozenset(inspect.signature(method).parameters)


def _api_error(e: Exception) -> DigikeyApiError:
    status = getattr(e, "status", None) or 0
    body = getattr(e, "body", None)
    headers = getattr(e, "headers", None) or {}
    detail = _problem_detail(body) or getattr(e, "reason", None) or "unknown error"
    if status == 429:
        retry_after = _int(next((v for k, v in headers.items() if k.lower() == "retry-after"), None))
        return DigikeyRateLimitError(status, detail, body=body, headers=headers, retry_after=retry_after)
    return DigikeyApiError(status, detail, body=body, headers=headers)


def _problem_detail(body: str | bytes | None) -> str | None:
    if not body:
        return None
    try:
        problem = json.loads(body)
    except ValueError:
        return body.decode(errors="replace")[:200] if isinstance(body, bytes) else body[:200]
    if not isinstance(problem, dict):
        return None
    parts = [str(problem[k]) for k in ("title", "detail") if problem.get(k)]
    errors = problem.get("errors")
    if errors:
        parts.append(json.dumps(errors))
    return " - ".join(parts) or None


def _int(value: str | None) -> int | None:
    try:
        return int(value) if value is not None else None
    except ValueError:
        return None


def _env_bool(name: str) -> bool:
    value = os.getenv(name, "").strip().lower()
    if value in ("", "0", "n", "no", "f", "false", "off"):
        return False
    if value in ("1", "y", "yes", "t", "true", "on"):
        return True
    raise DigikeyError(f"Invalid boolean for {name}: {value!r}")
