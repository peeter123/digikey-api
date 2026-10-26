# Generated DigiKey clients

`digikey/v4/*` is generated from the specs in `specs/` by `generate.py`, using a pinned
[openapi-generator](https://openapi-generator.tech) (`python` generator, pydantic v2). Never edit
the generated code by hand; CI regenerates it and fails on any difference.

| Spec | DigiKey API | Portal node | Package |
|---|---|---|---|
| `specs/productsearch.json` | [ProductSearch v4](https://developer.digikey.com/products/product-information-v4/productsearch) | 2357 | `digikey.v4.productsearch` |
| `specs/orderstatus.json` | [OrderStatus v4](https://developer.digikey.com/products/order-status/orderstatus) | 2291 | `digikey.v4.orderstatus` |

First downloaded 2026-10-26. The weekly `spec-drift` workflow downloads them again and opens a PR
when DigiKey changed anything.

## Commands

```sh
python openapi/generate.py           # regenerate from the committed specs (needs Java 11+)
python openapi/generate.py --fetch   # download the latest specs first
```

Specs come from the "Download Swagger File" button on the developer portal
(`https://developer.digikey.com/node/<node>/oas-download`, which needs a portal page as referer).
They are stored with normalised JSON formatting so spec changes show up as readable diffs.

## Preprocessing

Before generation, `enum` constraints on model properties are moved into the field description.
DigiKey adds enum values (order states, filter types) without a new API version, and generated
pydantic models would reject every response that contains a value they do not know.

## Adding a DigiKey API

1. Add an entry to `APIS` in `generate.py`: the portal node id (from the API's
   "Download Swagger File" link) and a portal page of that API.
2. Run `python openapi/generate.py --fetch`.
3. Add wrapper methods to `digikey/client.py` (and the base path in `DigikeyClient.__init__`).
4. Add unit tests and, if possible, a replay test; document it in the README and CHANGELOG.
