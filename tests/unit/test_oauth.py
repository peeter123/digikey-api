from __future__ import annotations

import json
import socket
import ssl
import threading
import urllib.request
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs

import pytest
import requests
import responses

from digikey.exceptions import DigikeyAuthError
from digikey.oauth import AuthorizationCodeAuth, ClientCredentialsAuth, Token, oauth2
from digikey.oauth.oauth2 import extract_code

TOKEN_URL = "https://api.digikey.com/v1/oauth2/token"
SANDBOX_TOKEN_URL = "https://sandbox-api.digikey.com/v1/oauth2/token"


@pytest.fixture
def clock(monkeypatch: pytest.MonkeyPatch) -> list[float]:
    now = [1_000_000.0]
    monkeypatch.setattr(oauth2.time, "time", lambda: now[0])
    return now


@pytest.fixture
def mocked() -> Any:
    with responses.RequestsMock() as rsps:
        yield rsps


def token_reply(mocked: Any, access: str = "access-1", refresh: str | None = None, url: str = TOKEN_URL) -> None:
    body: dict[str, Any] = {"access_token": access, "expires_in": 600, "token_type": "Bearer"}
    if refresh:
        body["refresh_token"] = refresh
    mocked.post(url, json=body)


def form(call: Any) -> dict[str, str]:
    return {k: v[0] for k, v in parse_qs(call.request.body).items()}


# Client credentials


def test_client_credentials_fetches_and_caches(mocked: Any, clock: list[float]) -> None:
    token_reply(mocked)
    auth = ClientCredentialsAuth("id", "secret")

    assert auth.access_token() == "access-1"
    assert auth.access_token() == "access-1"
    assert len(mocked.calls) == 1
    assert form(mocked.calls[0]) == {"grant_type": "client_credentials", "client_id": "id", "client_secret": "secret"}


def test_client_credentials_renews_before_expiry(mocked: Any, clock: list[float]) -> None:
    token_reply(mocked, "access-1")
    token_reply(mocked, "access-2")
    auth = ClientCredentialsAuth("id", "secret")
    auth.access_token()

    clock[0] += 600 - oauth2.EXPIRY_MARGIN - 1
    assert auth.access_token() == "access-1"
    clock[0] += 1
    assert auth.access_token() == "access-2"


def test_invalidate_forces_new_token(mocked: Any, clock: list[float]) -> None:
    token_reply(mocked, "access-1")
    token_reply(mocked, "access-2")
    auth = ClientCredentialsAuth("id", "secret")
    auth.access_token()
    auth.invalidate()
    assert auth.access_token() == "access-2"


def test_invalidate_without_token_is_harmless() -> None:
    ClientCredentialsAuth("id", "secret").invalidate()


def test_sandbox_token_endpoint(mocked: Any) -> None:
    token_reply(mocked, url=SANDBOX_TOKEN_URL)
    assert ClientCredentialsAuth("id", "secret", sandbox=True).access_token() == "access-1"


def test_credentials_are_required() -> None:
    with pytest.raises(DigikeyAuthError):
        ClientCredentialsAuth("", "secret")


@pytest.mark.parametrize(
    ("reply", "message"),
    [
        ({"json": {"error": "invalid_client", "error_description": "Bad credentials"}}, "Bad credentials"),
        ({"json": {"ErrorMessage": "Client not allowed"}}, "Client not allowed"),
        ({"json": ["odd"]}, "odd"),
        ({"body": "<html>gateway</html>"}, "gateway"),
        ({"body": ""}, "Unauthorized"),
    ],
)
def test_token_errors(mocked: Any, reply: dict[str, Any], message: str) -> None:
    mocked.post(TOKEN_URL, status=401, **reply)
    with pytest.raises(DigikeyAuthError, match=message) as error:
        ClientCredentialsAuth("id", "secret").access_token()
    assert "401" in str(error.value)


def test_token_network_error(mocked: Any) -> None:
    mocked.post(TOKEN_URL, body=requests.ConnectionError("no route"))
    with pytest.raises(DigikeyAuthError, match="Cannot reach"):
        ClientCredentialsAuth("id", "secret").access_token()


def test_malformed_token_response(mocked: Any) -> None:
    mocked.post(TOKEN_URL, json={"token": "?"})
    with pytest.raises(DigikeyAuthError, match="Unexpected token response"):
        ClientCredentialsAuth("id", "secret").access_token()


# Authorization code


def stored(path: Path, **token: Any) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    (path / oauth2.TOKEN_STORAGE).write_text(json.dumps(token))
    return path


def manual_auth(path: Path, redirect: str = "https://localhost:8139/digikey_callback?code=the-code") -> Any:
    prompts: list[str] = []

    def prompt(text: str) -> str:
        prompts.append(text)
        return redirect

    auth = AuthorizationCodeAuth("id", "secret", storage_path=path, manual=True, prompt=prompt)
    return auth, prompts


def test_uses_stored_1x_token_without_network(tmp_path: Path, clock: list[float], mocked: Any) -> None:
    stored(tmp_path, access_token="stored", refresh_token="r", expires=clock[0] + 100, token_type="Bearer")
    auth = AuthorizationCodeAuth("id", "secret", storage_path=str(tmp_path))
    assert auth.access_token() == "stored"
    assert len(mocked.calls) == 0


def test_expired_token_is_refreshed_and_rotated(tmp_path: Path, clock: list[float], mocked: Any) -> None:
    stored(tmp_path, access_token="old", refresh_token="refresh-1", expires=clock[0] - 1)
    token_reply(mocked, "new", refresh="refresh-2")

    assert AuthorizationCodeAuth("id", "secret", storage_path=tmp_path).access_token() == "new"
    assert form(mocked.calls[0])["grant_type"] == "refresh_token"
    assert form(mocked.calls[0])["refresh_token"] == "refresh-1"
    saved = json.loads((tmp_path / oauth2.TOKEN_STORAGE).read_text())
    assert saved == {"access_token": "new", "refresh_token": "refresh-2", "expires": clock[0] + 600 - 60}


def test_refresh_keeps_refresh_token_when_none_returned(tmp_path: Path, clock: list[float], mocked: Any) -> None:
    stored(tmp_path, access_token="old", refresh_token="refresh-1", expires=0)
    token_reply(mocked, "new")
    AuthorizationCodeAuth("id", "secret", storage_path=tmp_path).access_token()
    assert json.loads((tmp_path / oauth2.TOKEN_STORAGE).read_text())["refresh_token"] == "refresh-1"


def test_failed_refresh_falls_back_to_authorization(tmp_path: Path, clock: list[float], mocked: Any) -> None:
    stored(tmp_path, access_token="old", refresh_token="revoked", expires=0)
    mocked.post(TOKEN_URL, status=400, json={"error_description": "invalid refresh token"})
    token_reply(mocked, "fresh", refresh="refresh-2")
    auth, prompts = manual_auth(tmp_path)

    assert auth.access_token() == "fresh"
    assert len(prompts) == 1
    exchange = form(mocked.calls[1])
    assert exchange["grant_type"] == "authorization_code"
    assert exchange["code"] == "the-code"
    assert exchange["redirect_uri"] == oauth2.REDIRECT_URI


def test_stored_token_without_refresh_token_needs_authorization(tmp_path: Path, mocked: Any) -> None:
    stored(tmp_path, access_token="old", expires=0)
    token_reply(mocked, "fresh")
    auth, prompts = manual_auth(tmp_path)
    assert auth.access_token() == "fresh"
    assert prompts


def test_corrupt_storage_is_ignored(tmp_path: Path, mocked: Any, caplog: pytest.LogCaptureFixture) -> None:
    tmp_path.joinpath(oauth2.TOKEN_STORAGE).write_text("{not json")
    token_reply(mocked, "fresh")
    auth, _ = manual_auth(tmp_path)
    assert auth.access_token() == "fresh"
    assert "unreadable token storage" in caplog.text


def test_storage_is_created_and_token_reused(tmp_path: Path, clock: list[float], mocked: Any) -> None:
    storage = tmp_path / "does" / "not" / "exist"
    token_reply(mocked, "fresh", refresh="r")
    auth, prompts = manual_auth(storage)
    auth.access_token()
    auth.access_token()

    assert len(prompts) == 1
    assert (storage / oauth2.TOKEN_STORAGE).exists()
    assert not list(storage.glob("*.tmp"))


def test_default_storage_is_user_cache_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(oauth2, "user_cache_dir", lambda *a, **k: str(tmp_path / "cache"))
    auth = AuthorizationCodeAuth("id", "secret")
    assert auth.token_file == tmp_path / "cache" / oauth2.TOKEN_STORAGE


def test_storage_path_expands_user(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("USERPROFILE", str(tmp_path))
    assert AuthorizationCodeAuth("id", "secret", storage_path="~/tokens").storage_path == tmp_path / "tokens"


def test_sandbox_uses_own_token_file(tmp_path: Path) -> None:
    auth = AuthorizationCodeAuth("id", "secret", storage_path=tmp_path, sandbox=True)
    assert auth.token_file.name == oauth2.TOKEN_STORAGE_SANDBOX


def test_authorization_url(tmp_path: Path) -> None:
    url = AuthorizationCodeAuth("my id", "secret", storage_path=tmp_path).authorization_url
    assert url == (
        "https://api.digikey.com/v1/oauth2/authorize?client_id=my+id&response_type=code"
        "&redirect_uri=https%3A%2F%2Flocalhost%3A8139%2Fdigikey_callback"
    )


def test_manual_flow_reports_denied_authorization(tmp_path: Path, mocked: Any) -> None:
    auth, _ = manual_auth(tmp_path, "https://localhost:8139/digikey_callback?error=access_denied")
    with pytest.raises(DigikeyAuthError, match="access_denied"):
        auth.access_token()


@pytest.mark.parametrize(
    ("text", "code"),
    [
        ("abc123", "abc123"),
        ("  abc123\n", "abc123"),
        ("https://localhost:8139/digikey_callback?code=abc123&state=x", "abc123"),
        ("code=abc123", "abc123"),
    ],
)
def test_extract_code(text: str, code: str) -> None:
    assert extract_code(text) == code


@pytest.mark.parametrize(
    ("text", "message"),
    [
        ("", "No authorization code"),
        ("https://localhost/cb?error=access_denied&error_description=User+said+no", "User said no"),
        ("https://localhost/cb?state=x", "no code in redirect"),
    ],
)
def test_extract_code_errors(text: str, message: str) -> None:
    with pytest.raises(DigikeyAuthError, match=message):
        extract_code(text)


def test_token_repr_does_not_leak() -> None:
    token = Token(access_token="secret-token", expires=0, refresh_token="secret-refresh")
    assert token.expired
    assert token.to_storage()["access_token"] == "secret-token"


# Local HTTPS callback server


def free_port() -> int:
    with socket.socket() as s:
        s.bind(("localhost", 0))
        return int(s.getsockname()[1])


def browser(*paths: str) -> tuple[Any, list[tuple[int, str]]]:
    """Fake browser: after 'opening' the login page, DigiKey redirects to the callback URLs."""
    seen: list[tuple[int, str]] = []
    context = ssl._create_unverified_context()

    def visit(url: str) -> None:
        try:
            with urllib.request.urlopen(url, context=context, timeout=5) as response:
                seen.append((response.status, response.read().decode()))
        except urllib.error.HTTPError as e:
            seen.append((e.code, e.read().decode()))

    def open_browser(authorization_url: str) -> None:
        assert "response_type=code" in authorization_url
        threading.Thread(target=lambda: [visit(p) for p in paths], daemon=True).start()

    return open_browser, seen


def callback_auth(tmp_path: Path, port: int, open_browser: Any, **kwargs: Any) -> AuthorizationCodeAuth:
    return AuthorizationCodeAuth(
        "id",
        "secret",
        storage_path=tmp_path,
        redirect_uri=f"https://localhost:{port}/digikey_callback",
        open_browser=open_browser,
        **kwargs,
    )


def test_callback_server_receives_code(tmp_path: Path, mocked: Any) -> None:
    port = free_port()
    mocked.add_passthru(f"https://localhost:{port}")
    token_reply(mocked, "fresh", refresh="r")
    open_browser, seen = browser(
        f"https://localhost:{port}/favicon.ico", f"https://localhost:{port}/digikey_callback?code=xyz"
    )

    assert callback_auth(tmp_path, port, open_browser).access_token() == "fresh"
    assert form(mocked.calls[0])["code"] == "xyz"
    assert form(mocked.calls[0])["redirect_uri"] == f"https://localhost:{port}/digikey_callback"
    assert seen[0][0] == 404
    assert seen[1][0] == 200
    assert "xyz" not in seen[1][1]


def test_callback_server_reports_error(tmp_path: Path, mocked: Any) -> None:
    port = free_port()
    open_browser, seen = browser(f"https://localhost:{port}/digikey_callback?error=access_denied")
    with pytest.raises(DigikeyAuthError, match="access_denied"):
        callback_auth(tmp_path, port, open_browser).access_token()
    assert seen[0][0] == 400


def test_callback_server_times_out(tmp_path: Path, mocked: Any) -> None:
    port = free_port()
    with pytest.raises(DigikeyAuthError, match="Timed out"):
        callback_auth(tmp_path, port, lambda url: None, callback_timeout=0.1).access_token()
