from __future__ import annotations

from pathlib import Path
from typing import Any

import pydantic
import pytest
import urllib3

import digikey
from digikey import DigikeyApiError, DigikeyAuthError, DigikeyClient, DigikeyError, DigikeyRateLimitError
from digikey.oauth import AuthorizationCodeAuth, ClientCredentialsAuth
from digikey.v4 import productsearch
from tests.conftest import FakePoolManager, StaticAuth, make_client

PRODUCT = {
    "ManufacturerProductNumber": "CRCW080510K0FKEA",
    "Manufacturer": {"Id": 541, "Name": "Vishay Dale"},
    "Description": {"ProductDescription": "RES 10K OHM 1% 1/8W 0805"},
    "QuantityAvailable": 1234,
    "UnitPrice": 0.1,
    "ProductVariations": [{"DigiKeyProductNumber": "541-10.0KCCT-ND"}],
}


def test_keyword_search_sends_request_and_parses_response(client: DigikeyClient, http: FakePoolManager) -> None:
    http.reply(body={"Products": [PRODUCT], "ProductsCount": 1})

    result = client.keyword_search("CRCW080510K0FKEA")

    assert isinstance(result, productsearch.KeywordResponse)
    assert result.products_count == 1
    assert result.products[0].manufacturer.name == "Vishay Dale"
    request = http.last
    assert (request.method, request.url) == ("POST", "https://api.digikey.com/products/v4/search/keyword")
    assert request.json == {"Keywords": "CRCW080510K0FKEA"}
    assert request.headers["X-DIGIKEY-Client-Id"] == "my-client-id"
    assert request.headers["Authorization"] == "Bearer token-1"
    assert request.headers["User-Agent"].startswith("digikey-api/")


def test_keyword_search_accepts_request_model(client: DigikeyClient, http: FakePoolManager) -> None:
    client.keyword_search(productsearch.KeywordRequest(keywords="10k", limit=5, offset=10))
    assert http.last.json == {"Keywords": "10k", "Limit": 5, "Offset": 10}


def test_sandbox_uses_sandbox_host(auth: StaticAuth, http: FakePoolManager) -> None:
    client = make_client(auth, http, sandbox=True)
    client.product_details("P5555-ND")
    client.search_orders()
    assert [r.url.split("?")[0] for r in http.requests] == [
        "https://sandbox-api.digikey.com/products/v4/search/P5555-ND/productdetails",
        "https://sandbox-api.digikey.com/orderstatus/v4/orders",
    ]


@pytest.mark.parametrize(
    ("call", "method", "path"),
    [
        (lambda c: c.product_details("P5555-ND"), "GET", "/products/v4/search/P5555-ND/productdetails"),
        (lambda c: c.product_pricing("P5555-ND"), "GET", "/products/v4/search/P5555-ND/pricing"),
        (
            lambda c: c.pricing_options_by_quantity("P5555-ND", 100),
            "GET",
            "/products/v4/search/P5555-ND/pricingbyquantity/100",
        ),
        (lambda c: c.digi_reel_pricing("P5555-ND", 100), "GET", "/products/v4/search/P5555-ND/digireelpricing"),
        (lambda c: c.substitutions("P5555-ND"), "GET", "/products/v4/search/P5555-ND/substitutions"),
        (lambda c: c.recommended_products("P5555-ND"), "GET", "/products/v4/search/P5555-ND/recommendedproducts"),
        (lambda c: c.associations("P5555-ND"), "GET", "/products/v4/search/P5555-ND/associations"),
        (lambda c: c.alternate_packaging("P5555-ND"), "GET", "/products/v4/search/P5555-ND/alternatepackaging"),
        (lambda c: c.media("P5555-ND"), "GET", "/products/v4/search/P5555-ND/media"),
        (lambda c: c.manufacturers(), "GET", "/products/v4/search/manufacturers"),
        (lambda c: c.categories(), "GET", "/products/v4/search/categories"),
        (lambda c: c.categories_by_id(3), "GET", "/products/v4/search/categories/3"),
        (lambda c: c.search_orders(), "GET", "/orderstatus/v4/orders"),
        (lambda c: c.retrieve_sales_order(123), "GET", "/orderstatus/v4/salesorder/123"),
    ],
)
def test_every_method_reaches_its_endpoint_with_credentials(
    client: DigikeyClient, http: FakePoolManager, call: Any, method: str, path: str
) -> None:
    call(client)
    assert (http.last.method, http.last.path) == (method, path)
    assert http.last.headers["X-DIGIKEY-Client-Id"] == "my-client-id"
    assert http.last.headers["Authorization"] == "Bearer token-1"


def test_locale_and_account_headers_only_where_supported(auth: StaticAuth, http: FakePoolManager) -> None:
    client = make_client(auth, http, locale_site="NL", locale_language="nl", locale_currency="EUR", account_id="42")

    client.product_details("P5555-ND")
    details = http.last.headers
    client.media("P5555-ND")
    media = http.last.headers

    assert details["X-DIGIKEY-Locale-Site"] == "NL"
    assert details["X-DIGIKEY-Locale-Language"] == "nl"
    assert details["X-DIGIKEY-Locale-Currency"] == "EUR"
    assert details["X-DIGIKEY-Account-Id"] == "42"
    assert media["X-DIGIKEY-Locale-Site"] == "NL"
    assert "X-DIGIKEY-Account-Id" not in media


def test_unset_locale_headers_are_not_sent(client: DigikeyClient, http: FakePoolManager) -> None:
    client.product_details("P5555-ND")
    assert not any(h.startswith("X-DIGIKEY-Locale") for h in http.last.headers)


def test_per_call_parameters_override_defaults(auth: StaticAuth, http: FakePoolManager) -> None:
    client = make_client(auth, http, locale_currency="EUR")
    client.product_pricing("P5555-ND", in_stock=True, limit=3, x_digikey_locale_currency="USD")
    assert http.last.query == {"limit": ["3"], "inStock": ["true"]}
    assert http.last.headers["X-DIGIKEY-Locale-Currency"] == "USD"


def test_unknown_parameter_is_rejected(client: DigikeyClient) -> None:
    with pytest.raises(pydantic.ValidationError, match="bogus"):
        client.product_details("P5555-ND", bogus=1)


def test_unknown_enum_values_are_accepted(client: DigikeyClient, http: FakePoolManager) -> None:
    http.reply(body={"SalesOrderId": 1, "Status": {"SalesOrderStatus": "SomethingDigiKeyAddedLater"}})
    order = client.retrieve_sales_order(1)
    assert order.status.sales_order_status == "SomethingDigiKeyAddedLater"


def test_rate_limit_is_recorded(client: DigikeyClient, http: FakePoolManager) -> None:
    assert client.rate_limit == digikey.RateLimit()
    http.reply(headers={"X-RateLimit-Limit": "1000", "X-RateLimit-Remaining": "998"})
    client.categories()
    assert client.rate_limit == digikey.RateLimit(limit=1000, remaining=998)


def test_api_error_carries_problem_details(client: DigikeyClient, http: FakePoolManager) -> None:
    http.reply(404, {"title": "Not Found", "detail": "Product P0-ND not found", "status": 404})
    with pytest.raises(DigikeyApiError) as error:
        client.product_details("P0-ND")
    assert error.value.status == 404
    assert error.value.detail == "Not Found - Product P0-ND not found"
    assert "P0-ND" in str(error.value)
    assert "P0-ND" in error.value.body


def test_validation_errors_are_included(client: DigikeyClient, http: FakePoolManager) -> None:
    http.reply(400, {"title": "Bad Request", "errors": {"Limit": ["must be <= 50"]}})
    with pytest.raises(DigikeyApiError, match="must be <= 50"):
        client.keyword_search("x")


def test_non_json_error_body(client: DigikeyClient, http: FakePoolManager) -> None:
    http.reply(502, "<html>Bad gateway</html>")
    with pytest.raises(DigikeyApiError) as error:
        client.categories()
    assert error.value.status == 502
    assert error.value.detail == "<html>Bad gateway</html>"


def test_error_without_details_falls_back_to_reason(client: DigikeyClient, http: FakePoolManager) -> None:
    http.reply(503, "null")
    with pytest.raises(DigikeyApiError) as error:
        client.categories()
    assert error.value.status == 503
    assert error.value.detail == "Service Unavailable"


def test_rate_limit_error(client: DigikeyClient, http: FakePoolManager) -> None:
    http.reply(429, {"detail": "Too many requests"}, {"Retry-After": "30"})
    with pytest.raises(DigikeyRateLimitError) as error:
        client.categories()
    assert error.value.retry_after == 30
    assert error.value.headers["Retry-After"] == "30"


def test_rejected_token_is_renewed_once(client: DigikeyClient, auth: StaticAuth, http: FakePoolManager) -> None:
    http.reply(401, {"detail": "expired"}).reply(200, {"Categories": []})
    client.categories()
    assert [r.headers["Authorization"] for r in http.requests] == ["Bearer token-1", "Bearer token-2"]
    assert auth.invalidated == 1


def test_rejected_token_twice_raises(client: DigikeyClient, http: FakePoolManager) -> None:
    http.reply(401, {"detail": "nope"}).reply(401, {"detail": "nope"})
    with pytest.raises(DigikeyApiError) as error:
        client.categories()
    assert error.value.status == 401
    assert len(http.requests) == 2


def test_connection_errors_are_wrapped(client: DigikeyClient, http: FakePoolManager) -> None:
    http.reply(200, urllib3.exceptions.NewConnectionError(None, "connection refused"))  # type: ignore[arg-type]
    with pytest.raises(DigikeyError, match="Cannot reach"):
        client.categories()


@pytest.mark.parametrize(
    ("flow", "provider", "manual"),
    [
        ("client_credentials", ClientCredentialsAuth, None),
        ("authorization_code", AuthorizationCodeAuth, False),
        ("authorization_code_manual", AuthorizationCodeAuth, True),
    ],
)
def test_auth_flows(flow: Any, provider: type, manual: bool | None, tmp_path: Path) -> None:
    client = DigikeyClient("id", "secret", auth=flow, sandbox=True, storage_path=tmp_path)
    assert isinstance(client.auth, provider)
    assert client.auth.host == "https://sandbox-api.digikey.com"
    if manual is not None:
        assert client.auth.manual is manual
        assert client.auth.storage_path == tmp_path


def test_unknown_auth_flow() -> None:
    with pytest.raises(DigikeyAuthError, match="Unknown auth flow"):
        DigikeyClient("id", "secret", auth="password")  # type: ignore[arg-type]


def test_from_env_requires_credentials() -> None:
    with pytest.raises(DigikeyError, match="DIGIKEY_CLIENT_ID"):
        DigikeyClient.from_env()


def test_from_env(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    for name, value in {
        "DIGIKEY_CLIENT_ID": "env-id",
        "DIGIKEY_CLIENT_SECRET": "env-secret",
        "DIGIKEY_CLIENT_SANDBOX": "True",
        "DIGIKEY_AUTH_FLOW": "authorization_code",
        "DIGIKEY_STORAGE_PATH": str(tmp_path),
        "DIGIKEY_LOCALE_SITE": "DE",
        "DIGIKEY_ACCOUNT_ID": "7",
    }.items():
        monkeypatch.setenv(name, value)

    client = DigikeyClient.from_env(locale_currency="EUR")

    assert client.client_id == "env-id"
    assert client.sandbox is True
    assert isinstance(client.auth, AuthorizationCodeAuth)
    assert client.auth.storage_path == tmp_path
    assert client._headers["x_digikey_locale_site"] == "DE"
    assert client._headers["x_digikey_locale_currency"] == "EUR"
    assert client._headers["x_digikey_account_id"] == "7"


@pytest.mark.parametrize(("value", "expected"), [("", False), ("0", False), ("false", False), ("YES", True)])
def test_from_env_sandbox_values(monkeypatch: pytest.MonkeyPatch, value: str, expected: bool) -> None:
    monkeypatch.setenv("DIGIKEY_CLIENT_ID", "id")
    monkeypatch.setenv("DIGIKEY_CLIENT_SECRET", "secret")
    monkeypatch.setenv("DIGIKEY_CLIENT_SANDBOX", value)
    assert DigikeyClient.from_env().sandbox is expected


def test_from_env_invalid_bool(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DIGIKEY_CLIENT_ID", "id")
    monkeypatch.setenv("DIGIKEY_CLIENT_SECRET", "secret")
    monkeypatch.setenv("DIGIKEY_CLIENT_SANDBOX", "maybe")
    with pytest.raises(DigikeyError, match="DIGIKEY_CLIENT_SANDBOX"):
        DigikeyClient.from_env()


def test_garbage_rate_limit_headers_are_ignored() -> None:
    assert digikey.RateLimit.from_headers({"X-RateLimit-Limit": "lots"}) == digikey.RateLimit()
    assert digikey.RateLimit.from_headers(None) == digikey.RateLimit()


@pytest.mark.parametrize(
    ("body", "detail"),
    [(None, None), (b"", None), (b"plain text", "plain text"), ('{"detail": "x"}', "x"), ("{}", None)],
)
def test_problem_detail(body: Any, detail: str | None) -> None:
    from digikey.client import _problem_detail

    assert _problem_detail(body) == detail
