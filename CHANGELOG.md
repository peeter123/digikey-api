# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[semantic versioning](https://semver.org/).

## [Unreleased]

## [2.0.0] - unreleased

A rewrite on DigiKey's v4 APIs. See "Migrating from 1.x" in the README.

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
- Module-level functions (`digikey.keyword_search` etc.) call the v4 APIs and use v4 models.
- Errors are raised instead of logged and returned as `None`.
- The token storage directory is created when missing and defaults to the user cache directory.
- Refresh tokens are rotated and saved after every refresh.
- The local OAuth callback certificate is made with `cryptography` (fixes Python 3.13+).

### Removed
- DigiKey v3 APIs (`digikey.v3`), including `suggested_parts`, `manufacturer_product_details` and
  `batch_product_details`, which have no v4 equivalent.
- The `api_limits` and `status` dict arguments.
- Dependencies `certauth`, `retrying`, `inflection`.

Thanks to @hurricaneJoef (#51) and @flaviut (#54) for the first v4 ports.

## [1.1.0] - 2024-11-22

### Fixed
- Python 3.12 compatibility (`distutils` and `ssl.wrap_socket` removed).

Older releases: see the [git history](https://github.com/peeter123/digikey-api/commits/v1.x).
