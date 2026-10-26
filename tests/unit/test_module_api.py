"""The module-level functions kept for digikey-api 1.x scripts."""

from __future__ import annotations

import pytest

import digikey
from digikey.v4 import productsearch
from tests.conftest import FakePoolManager, StaticAuth, make_client


@pytest.fixture
def http(monkeypatch: pytest.MonkeyPatch) -> FakePoolManager:
    http = FakePoolManager()
    monkeypatch.setenv("DIGIKEY_CLIENT_ID", "env-id")
    monkeypatch.setenv("DIGIKEY_CLIENT_SECRET", "env-secret")
    monkeypatch.setattr(digikey.DigikeyClient, "from_env", classmethod(lambda cls: make_client(StaticAuth(), http)))
    return http


def test_default_client_is_reused_until_env_changes(http: FakePoolManager, monkeypatch: pytest.MonkeyPatch) -> None:
    first = digikey.default_client()
    assert digikey.default_client() is first
    monkeypatch.setenv("DIGIKEY_CLIENT_SANDBOX", "true")
    assert digikey.default_client() is not first


def test_keyword_search_with_1x_body_argument(http: FakePoolManager) -> None:
    digikey.keyword_search(body=productsearch.KeywordRequest(keywords="10k"))
    assert http.last.json == {"Keywords": "10k"}


def test_keyword_search_needs_a_request(http: FakePoolManager) -> None:
    with pytest.raises(digikey.DigikeyError):
        digikey.keyword_search()


@pytest.mark.parametrize(
    ("call", "path"),
    [
        (lambda: digikey.keyword_search("10k"), "/products/v4/search/keyword"),
        (lambda: digikey.product_details("P5555-ND"), "/products/v4/search/P5555-ND/productdetails"),
        (lambda: digikey.digi_reel_pricing("P5555-ND", 10), "/products/v4/search/P5555-ND/digireelpricing"),
        (lambda: digikey.status_salesorder_id(5), "/orderstatus/v4/salesorder/5"),
        (lambda: digikey.salesorder_history(start_date="2026-01-01"), "/orderstatus/v4/orders"),
    ],
)
def test_module_functions(http: FakePoolManager, call: object, path: str) -> None:
    call()  # type: ignore[operator]
    assert http.last.path == path


def test_salesorder_history_passes_dates(http: FakePoolManager) -> None:
    digikey.salesorder_history(start_date="2026-01-01", end_date="2026-02-01")
    assert http.last.query["StartDate"][0].startswith("2026-01-01")
    assert http.last.query["EndDate"][0].startswith("2026-02-01")


def test_1x_exception_name_still_works() -> None:
    assert digikey.DigikeyOauthException is digikey.DigikeyAuthError
