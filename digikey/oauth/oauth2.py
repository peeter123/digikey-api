"""OAuth2 token providers for the DigiKey API.

Two flows are supported, see https://developer.digikey.com/documentation:

* :class:`ClientCredentialsAuth` (2-legged): headless, no user interaction and nothing stored on disk.
* :class:`AuthorizationCodeAuth` (3-legged): a DigiKey user logs in once in a browser, after which the
  refresh token is stored and used. Needed for customer-specific data such as ``MyPricing``.

Any object with an ``access_token() -> str`` and ``invalidate()`` method can be used as provider.
"""

from __future__ import annotations

import datetime
import json
import logging
import os
import ssl
import tempfile
import threading
import time
import webbrowser
from collections.abc import Callable
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any, Protocol
from urllib.parse import parse_qs, urlencode, urlparse

import requests
from platformdirs import user_cache_dir

from digikey.exceptions import DigikeyAuthError

PROD_HOST = "https://api.digikey.com"
SANDBOX_HOST = "https://sandbox-api.digikey.com"
TOKEN_PATH = "/v1/oauth2/token"
AUTHORIZE_PATH = "/v1/oauth2/authorize"

REDIRECT_URI = "https://localhost:8139/digikey_callback"
TOKEN_STORAGE = "token_storage.json"
TOKEN_STORAGE_SANDBOX = "token_storage_sandbox.json"

# Tokens are renewed this many seconds before they really expire.
EXPIRY_MARGIN = 60

logger = logging.getLogger(__name__)


class TokenProvider(Protocol):
    def access_token(self) -> str:
        """Return a valid access token, obtaining or refreshing one when needed."""
        ...

    def invalidate(self) -> None:
        """Forget the current access token, e.g. after the API rejected it."""
        ...


@dataclass
class Token:
    access_token: str
    expires: float
    refresh_token: str | None = None

    @classmethod
    def from_response(cls, data: dict[str, Any]) -> Token:
        return cls(
            access_token=data["access_token"],
            expires=time.time() + int(data["expires_in"]) - EXPIRY_MARGIN,
            refresh_token=data.get("refresh_token"),
        )

    @classmethod
    def from_storage(cls, data: dict[str, Any]) -> Token:
        # Same layout as digikey-api 1.x, so existing token storage keeps working.
        return cls(
            access_token=data["access_token"], expires=float(data["expires"]), refresh_token=data.get("refresh_token")
        )

    def to_storage(self) -> dict[str, Any]:
        return {"access_token": self.access_token, "expires": self.expires, "refresh_token": self.refresh_token}

    @property
    def expired(self) -> bool:
        return time.time() >= self.expires


class _OAuth2:
    def __init__(self, client_id: str, client_secret: str, *, sandbox: bool = False, timeout: float = 30) -> None:
        if not client_id or not client_secret:
            raise DigikeyAuthError("A DigiKey client id and client secret are required")
        self.client_id = client_id
        self.client_secret = client_secret
        self.host = SANDBOX_HOST if sandbox else PROD_HOST
        self.timeout = timeout
        self._token: Token | None = None
        self._lock = threading.Lock()

    def invalidate(self) -> None:
        with self._lock:
            if self._token is not None:
                self._token.expires = 0

    def _request_token(self, data: dict[str, str]) -> Token:
        data = {**data, "client_id": self.client_id, "client_secret": self.client_secret}
        try:
            response = requests.post(self.host + TOKEN_PATH, data=data, timeout=self.timeout)
        except requests.RequestException as e:
            raise DigikeyAuthError(f"Cannot reach the DigiKey token endpoint: {e}") from e
        if not response.ok:
            raise DigikeyAuthError(
                f"DigiKey refused the {data['grant_type']} token request ({response.status_code}): "
                f"{_error_description(response)}"
            )
        try:
            token = Token.from_response(response.json())
        except (ValueError, KeyError, TypeError) as e:
            raise DigikeyAuthError(f"Unexpected token response from DigiKey: {e!r}") from e
        logger.debug("Obtained %s access token valid until %s", data["grant_type"], _timestamp(token.expires))
        return token


class ClientCredentialsAuth(_OAuth2):
    """2-legged OAuth2: the app authenticates itself, no user login and no storage needed."""

    def access_token(self) -> str:
        with self._lock:
            if self._token is None or self._token.expired:
                self._token = self._request_token({"grant_type": "client_credentials"})
            return self._token.access_token


class AuthorizationCodeAuth(_OAuth2):
    """3-legged OAuth2: a DigiKey user authorizes the app once, the refresh token is stored.

    ``storage_path`` is the directory for the token file, by default the user cache dir. It is
    created when missing. With ``manual=True`` no local server is started: the authorization URL
    is printed and the URL the browser was redirected to has to be pasted back, which works on
    headless machines. The redirect URI must match the OAuth callback registered for the app.
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        *,
        sandbox: bool = False,
        storage_path: str | os.PathLike[str] | None = None,
        manual: bool = False,
        redirect_uri: str = REDIRECT_URI,
        open_browser: Callable[[str], object] = webbrowser.open_new,
        prompt: Callable[[str], str] = input,
        callback_timeout: float = 300,
        timeout: float = 30,
    ) -> None:
        super().__init__(client_id, client_secret, sandbox=sandbox, timeout=timeout)
        self.storage_path = (
            Path(storage_path).expanduser() if storage_path else Path(user_cache_dir("digikey-api", appauthor=False))
        )
        self.token_file = self.storage_path / (TOKEN_STORAGE_SANDBOX if sandbox else TOKEN_STORAGE)
        self.manual = manual
        self.redirect_uri = redirect_uri
        self.open_browser = open_browser
        self.prompt = prompt
        self.callback_timeout = callback_timeout
        self._loaded = False

    @property
    def authorization_url(self) -> str:
        query = urlencode({"client_id": self.client_id, "response_type": "code", "redirect_uri": self.redirect_uri})
        return f"{self.host}{AUTHORIZE_PATH}?{query}"

    def access_token(self) -> str:
        with self._lock:
            if not self._loaded:
                self._token = self._load()
                self._loaded = True
            if self._token is not None and not self._token.expired:
                return self._token.access_token
            token = self._refresh(self._token) if self._token is not None else None
            if token is None:
                token = self._request_token(
                    {"grant_type": "authorization_code", "code": self._authorize(), "redirect_uri": self.redirect_uri}
                )
            self._token = token
            self._save(token)
            return token.access_token

    def _refresh(self, token: Token) -> Token | None:
        if not token.refresh_token:
            return None
        try:
            new = self._request_token({"grant_type": "refresh_token", "refresh_token": token.refresh_token})
        except DigikeyAuthError as e:
            logger.warning("Refreshing the DigiKey token failed, a new authorization is needed: %s", e)
            return None
        # DigiKey rotates refresh tokens; keep the old one if the response has none.
        new.refresh_token = new.refresh_token or token.refresh_token
        return new

    def _load(self) -> Token | None:
        try:
            return Token.from_storage(json.loads(self.token_file.read_text(encoding="utf-8")))
        except FileNotFoundError:
            return None
        except (OSError, ValueError, KeyError, TypeError) as e:
            logger.warning("Ignoring unreadable token storage %s: %r", self.token_file, e)
            return None

    def _save(self, token: Token) -> None:
        self.storage_path.mkdir(parents=True, exist_ok=True)
        tmp = self.token_file.with_suffix(".tmp")
        tmp.write_text(json.dumps(token.to_storage()), encoding="utf-8")
        tmp.chmod(0o600)
        tmp.replace(self.token_file)

    def _authorize(self) -> str:
        if self.manual:
            print(f"Open this URL in a browser and log in to DigiKey:\n\n    {self.authorization_url}\n")
            return extract_code(self.prompt("Paste the URL you were redirected to: "))
        return self._receive_code()

    def _receive_code(self) -> str:
        """Run a one-shot HTTPS server on the redirect URI and wait for DigiKey to call it."""
        redirect = urlparse(self.redirect_uri)
        result: dict[str, str] = {}

        class CallbackHandler(BaseHTTPRequestHandler):
            def do_GET(self) -> None:
                url = urlparse(self.path)
                if url.path != redirect.path:
                    self.send_error(404)
                    return
                try:
                    result["code"] = extract_code(self.path)
                    status, message = 200, "Authorization complete, you may close this window."
                except DigikeyAuthError as e:
                    result["error"] = str(e)
                    status, message = 400, "Authorization failed, see the application output."
                self.send_response(status)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(f"<html><body><h1>{message}</h1></body></html>".encode())

            def log_message(self, format: str, *args: Any) -> None:
                pass

        with tempfile.TemporaryDirectory() as tmp:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(*_self_signed_certificate(Path(tmp), redirect.hostname or "localhost"))
            server = HTTPServer((redirect.hostname or "localhost", redirect.port or 443), CallbackHandler)
            server.socket = context.wrap_socket(server.socket, server_side=True)
            server.timeout = 1
            try:
                print(
                    f"Opening a browser to log in to DigiKey. If it does not open, visit:\n    {self.authorization_url}"
                )
                self.open_browser(self.authorization_url)
                deadline = time.monotonic() + self.callback_timeout
                while not result and time.monotonic() < deadline:
                    server.handle_request()
            finally:
                server.server_close()

        if "code" in result:
            return result["code"]
        raise DigikeyAuthError(result.get("error", "Timed out waiting for the DigiKey authorization callback"))


def extract_code(redirected: str) -> str:
    """Get the authorization code from a redirect URL (or a bare code)."""
    redirected = redirected.strip()
    if "?" not in redirected and "=" not in redirected:
        if not redirected:
            raise DigikeyAuthError("No authorization code given")
        return redirected
    query = parse_qs(urlparse(redirected).query or redirected.split("?", 1)[-1])
    if "code" in query:
        return query["code"][0]
    error = query.get("error_description", query.get("error", ["no code in redirect"]))[0]
    raise DigikeyAuthError(f"DigiKey authorization failed: {error}")


def _error_description(response: requests.Response) -> str:
    try:
        body = response.json()
    except ValueError:
        return response.text[:200] or response.reason
    if isinstance(body, dict):
        for key in ("error_description", "detail", "ErrorMessage", "error"):
            if body.get(key):
                return str(body[key])
    return str(body)[:200]


def _timestamp(epoch: float) -> str:
    return datetime.datetime.fromtimestamp(epoch).astimezone().isoformat(timespec="seconds")


def _self_signed_certificate(directory: Path, hostname: str) -> tuple[str, str]:
    """Write a throw-away certificate for the local callback server, return (certfile, keyfile)."""
    import ipaddress

    from cryptography import x509
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.x509.oid import NameOID

    key = ec.generate_private_key(ec.SECP256R1())
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, hostname)])
    now = datetime.datetime.now(datetime.timezone.utc)
    certificate = (
        x509.CertificateBuilder()
        .subject_name(name)
        .issuer_name(name)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - datetime.timedelta(minutes=5))
        .not_valid_after(now + datetime.timedelta(days=1))
        .add_extension(
            x509.SubjectAlternativeName([x509.DNSName(hostname), x509.IPAddress(ipaddress.ip_address("127.0.0.1"))]),
            critical=False,
        )
        .sign(key, hashes.SHA256())
    )
    certfile, keyfile = directory / "cert.pem", directory / "key.pem"
    certfile.write_bytes(certificate.public_bytes(serialization.Encoding.PEM))
    keyfile.write_bytes(
        key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption())
    )
    return str(certfile), str(keyfile)
