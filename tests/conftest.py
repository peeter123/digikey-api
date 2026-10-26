from __future__ import annotations

import json
from dataclasses import dataclass, field
from http import HTTPStatus
from typing import Any
from urllib.parse import parse_qs, urlparse

import pytest
import urllib3

import digikey


@pytest.fixture(autouse=True)
def clean_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Tests never see the developer's real DigiKey settings."""
    for name in digikey._ENV:
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setattr(digikey, "_default", None)


class StaticAuth:
    """Token provider handing out numbered tokens, counts invalidations."""

    def __init__(self) -> None:
        self.issued = 0
        self.invalidated = 0

    def access_token(self) -> str:
        if self.issued == self.invalidated:
            self.issued += 1
        return f"token-{self.issued}"

    def invalidate(self) -> None:
        self.invalidated = self.issued


@dataclass
class Request:
    method: str
    url: str
    headers: dict[str, str]
    body: Any

    @property
    def path(self) -> str:
        return urlparse(self.url).path

    @property
    def query(self) -> dict[str, list[str]]:
        return parse_qs(urlparse(self.url).query)

    @property
    def json(self) -> Any:
        return json.loads(self.body)


@dataclass
class FakePoolManager:
    """Stands in for urllib3 below the generated clients: the whole generated stack still runs."""

    responses: list[tuple[int, Any, dict[str, str]]] = field(default_factory=list)
    requests: list[Request] = field(default_factory=list)

    def reply(self, status: int = 200, body: Any = None, headers: dict[str, str] | None = None) -> FakePoolManager:
        self.responses.append((status, {} if body is None else body, headers or {}))
        return self

    def request(self, method: str, url: str, body: Any = None, headers: Any = None, **_: Any) -> urllib3.HTTPResponse:
        self.requests.append(Request(method, url, dict(headers or {}), body))
        status, payload, extra = self.responses.pop(0) if self.responses else (200, {}, {})
        if isinstance(payload, Exception):
            raise payload
        raw = payload if isinstance(payload, (str, bytes)) else json.dumps(payload)
        raw = raw.encode() if isinstance(raw, str) else raw
        return urllib3.HTTPResponse(
            body=raw,
            status=status,
            reason=HTTPStatus(status).phrase,
            headers={"Content-Type": "application/json", **extra},
            preload_content=True,
        )

    @property
    def last(self) -> Request:
        return self.requests[-1]


@pytest.fixture
def auth() -> StaticAuth:
    return StaticAuth()


@pytest.fixture
def http() -> FakePoolManager:
    return FakePoolManager()


@pytest.fixture
def client(auth: StaticAuth, http: FakePoolManager) -> digikey.DigikeyClient:
    return make_client(auth, http)


def make_client(auth: StaticAuth, http: FakePoolManager, **kwargs: Any) -> digikey.DigikeyClient:
    client = digikey.DigikeyClient("my-client-id", "my-secret", auth=auth, **kwargs)
    for api in (client.product_search_api, client.order_history_api):
        api.api_client.rest_client.pool_manager = http
    return client
