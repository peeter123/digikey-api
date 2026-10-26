# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[semantic versioning](https://semver.org/).

## [Unreleased]

## [2.0.0] - unreleased

A rewrite on DigiKey's v4 APIs. See "Migrating from 1.x" in the README. If you need the v3 APIs,
pin `digikey-api<2`. DigiKey no longer serves most of v3.

### Breaking changes
- **DigiKey v4 APIs and models.** All requests and responses use the v4 models from
  `digikey.v4.productsearch` and `digikey.v4.orderstatus`, and `digikey.v3` is gone. Field names
  follow the v4 schema, for example `KeywordSearchRequest(record_count=...)` becomes
  `KeywordRequest(limit=...)`.
- **Removed functions:** `suggested_parts`, `manufacturer_product_details` and `batch_product_details`.
  v4 has no equivalent; use `recommended_products` / `substitutions`, `keyword_search` and
  `product_details`.
- **Different return types:** `status_salesorder_id` returns a v4 `SalesOrder` and
  `salesorder_history` returns a v4 `OrderResponse`.
- **Errors raise exceptions.** API errors raise `DigikeyApiError` (or `DigikeyRateLimitError`)
  instead of being logged and returned as `None`.
- **No more `api_limits={}` / `status={}` arguments.** Read `client.rate_limit` and
  `DigikeyApiError.status` instead.
- **New default OAuth flow.** It is now 2-legged `client_credentials` instead of the browser login.
  Apps that are only allowed the authorization code flow, and anything that needs `MyPricing`, must set
  `DIGIKEY_AUTH_FLOW=authorization_code` (or pass `auth="authorization_code"`).
- **OrderStatus with `client_credentials` needs an account id.** Pass `account_id=` or set
  `DIGIKEY_ACCOUNT_ID`.
- **Sandbox tokens are stored separately.** They now go in `token_storage_sandbox.json`, so sandbox
  users log in once again. Production `token_storage.json` files keep working.
- **Python 3.10 or newer is required.**
- **Removed internals:** `digikey.oauth.oauth2.TokenHandler` and `Oauth2Token` (replaced by
  `ClientCredentialsAuth` / `AuthorizationCodeAuth`), `digikey.utils`, `digikey.constants`,
  `digikey.decorators`, `DigikeyTypeError` and the `digikey.name` attribute.
- **Dropped dependencies:** `certauth`, `retrying` and `inflection` are no longer installed. Code
  that imported them through this package must depend on them directly.

### Added
- `DigikeyClient` with credentials, sandbox, locale and account settings passed as arguments (or
  `DigikeyClient.from_env()`), covering all ProductSearch v4 and OrderStatus v4 endpoints.
- 2-legged OAuth2 (client credentials), now the default: works headless with nothing stored on disk.
- `authorization_code_manual` flow for 3-legged login on headless machines.
- Exceptions `DigikeyApiError` (with `status`, `detail`, `body`), `DigikeyRateLimitError` (with
  `retry_after`) and `DigikeyAuthError`; `client.rate_limit` with the rate limit headers.
- Type hints (`py.typed`) and Python 3.10–3.14 support.
- Clients generated from DigiKey's committed OpenAPI specs, regenerated weekly when DigiKey changes them.

### Changed
- The token storage directory is created when missing, `~` is expanded, and it defaults to the user
  cache directory.
- Refresh tokens are rotated and saved after every refresh.
- The local OAuth callback certificate is made with `cryptography` (fixes Python 3.13+).
- `DigikeyOauthException` is now an alias of `DigikeyAuthError`, a subclass of `DigikeyError`.

Thanks to @hurricaneJoef (#51) and @flaviut (#54) for the first v4 ports.

## [1.1.0] - 2024-11-22

### Fixed
- Python 3.12 compatibility (`distutils` and `ssl.wrap_socket` removed).

Older releases: see the [git history](https://github.com/peeter123/digikey-api/commits/v1.x).
