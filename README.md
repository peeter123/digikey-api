Python Client for the DigiKey API
=================================
Search the DigiKey catalog, get real-time pricing and availability, and look up your orders with
the DigiKey v4 APIs.

[![PyPI](https://img.shields.io/pypi/v/digikey-api.svg?color=brightgreen)](https://pypi.org/project/digikey-api/)
[![CI](https://github.com/peeter123/digikey-api/actions/workflows/ci.yml/badge.svg)](https://github.com/peeter123/digikey-api/actions/workflows/ci.yml)
[![Live API](https://github.com/peeter123/digikey-api/actions/workflows/live.yml/badge.svg)](https://github.com/peeter123/digikey-api/actions/workflows/live.yml)
[![Donate](https://img.shields.io/badge/Donate-PayPal-gold.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=53HWHHVCJ3D4J&currency_code=EUR&source=url)

Supported APIs (Python 3.10+):

* [ProductSearch v4](https://developer.digikey.com/products/product-information-v4/productsearch): keyword
  search, product details, pricing, DigiReel pricing, substitutions, recommended products,
  associations, alternate packaging, media, manufacturers and categories.
* [OrderStatus v4](https://developer.digikey.com/products/order-status/orderstatus): order history and
  sales order details.

The clients are generated from DigiKey's published OpenAPI specs, which are checked weekly for changes.
Other DigiKey APIs can be added the same way, see [CONTRIBUTING.md](CONTRIBUTING.md).

> **digikey-api 2.0 uses DigiKey's v4 APIs.** The v3 APIs are no longer supported; stay on
> `digikey-api<2` if you need them (that version is frozen). See [Migrating from 1.x](#migrating-from-1x).

# Quickstart

```sh
pip install digikey-api
```

Register an app on the [DigiKey developer portal](https://developer.digikey.com/get_started) and note its
client ID and secret. Use a production app for real data; sandbox apps return dummy data.

```python
from digikey import DigikeyClient

client = DigikeyClient("client_id", "client_secret")

# Search for parts
result = client.keyword_search("CRCW080510K0FKEA")
for product in result.products:
    print(product.manufacturer_product_number, product.unit_price, product.quantity_available)

# Full details and pricing for one part
details = client.product_details("296-6501-1-ND")
print(details.product.description.product_description)

# Optional parameters use the names of the DigiKey API
pricing = client.product_pricing("296-6501-1-ND", in_stock=True, limit=5)

# More control over the search
from digikey.v4.productsearch import KeywordRequest

result = client.keyword_search(KeywordRequest(keywords="10k 0805", limit=50, offset=0))
```

Responses are pydantic models from `digikey.v4.productsearch` and `digikey.v4.orderstatus`
(`.to_dict()` and `.to_json()` give plain data). Errors raise exceptions:

```python
from digikey import DigikeyApiError, DigikeyRateLimitError

try:
    client.product_details("does-not-exist")
except DigikeyRateLimitError as e:
    print("slow down, retry after", e.retry_after)
except DigikeyApiError as e:
    print(e.status, e.detail)

print(client.rate_limit)  # RateLimit(limit=1000, remaining=998) from the last response
```

## Authentication

DigiKey uses OAuth2. Pick the flow with `auth=`:

| `auth=` | Flow | Use for |
|---|---|---|
| `"client_credentials"` (default) | 2-legged | Scripts, servers and CI. No browser, nothing stored on disk. |
| `"authorization_code"` | 3-legged | Data tied to your DigiKey account, such as `MyPricing`. Opens a browser once. |
| `"authorization_code_manual"` | 3-legged | The same on a headless machine: open the printed URL anywhere and paste back the URL you were redirected to. |

Your app must be subscribed to each API product it calls (ProductSearch v4, OrderStatus v4) on the
developer portal, or DigiKey answers `401 Invalid clientId. X-DIGIKEY-Client-Id invalid for requested
resource`. With `client_credentials` there is no logged-in user, so OrderStatus also needs
`account_id=` (your DigiKey account number).

For the 3-legged flows, set the app's OAuth callback to `https://localhost:8139/digikey_callback`. The
token is stored in `storage_path` (by default the user cache directory, e.g.
`~/.cache/digikey-api`) and refreshed automatically, so you only log in again when the refresh token
expires. Your browser will warn about the self-signed certificate of the local callback page; that is
expected.

```python
client = DigikeyClient("client_id", "client_secret", auth="authorization_code", storage_path="~/.digikey")
```

## Settings

```python
client = DigikeyClient(
    "client_id",
    "client_secret",
    sandbox=False,  # use sandbox-api.digikey.com
    locale_site="NL",  # X-DIGIKEY-Locale-Site
    locale_language="en",  # X-DIGIKEY-Locale-Language
    locale_currency="EUR",  # X-DIGIKEY-Locale-Currency
    account_id="123456",  # X-DIGIKEY-Account-Id, for account specific pricing
    timeout=30,  # seconds per request
)
```

`DigikeyClient.from_env()` reads the same settings from environment variables:

| Variable | Meaning |
|---|---|
| `DIGIKEY_CLIENT_ID`, `DIGIKEY_CLIENT_SECRET` | App credentials (required) |
| `DIGIKEY_CLIENT_SANDBOX` | `true` to use the sandbox |
| `DIGIKEY_AUTH_FLOW` | `client_credentials` (default), `authorization_code` or `authorization_code_manual` |
| `DIGIKEY_STORAGE_PATH` | Token storage directory for the 3-legged flows |
| `DIGIKEY_LOCALE_SITE`, `DIGIKEY_LOCALE_LANGUAGE`, `DIGIKEY_LOCALE_CURRENCY`, `DIGIKEY_ACCOUNT_ID` | Optional headers |

## Methods

| ProductSearch | OrderStatus |
|---|---|
| `keyword_search(request_or_keyword)` | `search_orders(start_date=, end_date=, page_number=, page_size=, shared=)` |
| `product_details(product_number)` | `retrieve_sales_order(sales_order_id)` |
| `product_pricing(product_number)` | |
| `pricing_options_by_quantity(product_number, quantity)` | |
| `digi_reel_pricing(product_number, quantity)` | |
| `substitutions(product_number)` | |
| `recommended_products(product_number)` | |
| `associations(product_number)` | |
| `alternate_packaging(product_number)` | |
| `media(product_number)` | |
| `manufacturers()`, `categories()`, `categories_by_id(category_id)` | |

The generated API classes are available too (`client.product_search_api`, `client.order_history_api`)
if you need something the wrapper does not expose.

## Logging

Logging is not forced upon the user but can be enabled according to convention:

```python
import logging

logging.getLogger("digikey").setLevel(logging.DEBUG)
logging.basicConfig()
```

Tokens and secrets are never logged.

# Migrating from 1.x

The module-level functions still exist and read the same environment variables as before, but they
now call the v4 APIs, so **request and response models changed**: field names follow DigiKey's v4
schema (for example `KeywordRequest(keywords=..., limit=...)` instead of
`KeywordSearchRequest(keywords=..., record_count=...)`).

| 1.x | 2.x |
|---|---|
| `digikey.keyword_search(body=KeywordSearchRequest(...))` | `client.keyword_search(KeywordRequest(...))` (`digikey.keyword_search(body=...)` still works) |
| `digikey.product_details(dkpn)` | `client.product_details(dkpn)` |
| `digikey.digi_reel_pricing(dkpn, qty)` | `client.digi_reel_pricing(dkpn, qty)` |
| `digikey.suggested_parts(dkpn)` | `client.recommended_products(dkpn)` or `client.substitutions(dkpn)` |
| `digikey.manufacturer_product_details(body=...)` | `client.keyword_search(...)` or `client.product_details(mpn)` |
| `digikey.batch_product_details(body=...)` | `client.product_details(...)` per part (v4 has no batch endpoint) |
| `digikey.status_salesorder_id(id)` | `client.retrieve_sales_order(id)` |
| `digikey.salesorder_history(start_date=, end_date=)` | `client.search_orders(start_date=, end_date=)` |
| `api_limits={}` / `status={}` arguments | `client.rate_limit`; errors raise `DigikeyApiError` with `.status` |
| Functions returned `None` on API errors | Errors raise `DigikeyApiError` |
| Browser login always required | `client_credentials` is the default; set `DIGIKEY_AUTH_FLOW=authorization_code` for the 1.x behaviour |
| `DIGIKEY_STORAGE_PATH` had to exist | Created when needed, defaults to the user cache directory |
| `digikey.v3.*` | `digikey.v4.productsearch`, `digikey.v4.orderstatus` |
| OrderStatus with your login | With `client_credentials` also pass `account_id=` (or set `DIGIKEY_ACCOUNT_ID`) |
| `digikey.oauth.oauth2.TokenHandler` | `ClientCredentialsAuth`, `AuthorizationCodeAuth` |
| Python 3.6+ | Python 3.10+ |

Existing production `token_storage.json` files from 1.x keep working with the 3-legged flows. Sandbox
tokens now live in `token_storage_sandbox.json`, so sandbox users log in once again. The complete list
of breaking changes is in the [CHANGELOG](CHANGELOG.md#200---unreleased).

# Contributing

Bug reports and PRs are welcome, see [CONTRIBUTING.md](CONTRIBUTING.md). Thanks to
[@hurricaneJoef](https://github.com/hurricaneJoef) and [@flaviut](https://github.com/flaviut), whose v4
work in #51 and #54 paved the way for 2.0.
