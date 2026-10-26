# Contributing

Thanks for helping! This project is maintained with as little manual work as possible, so the
tooling does most of the checking. Please read [AGENTS.md](AGENTS.md) for the rules; they apply to
humans too.

## Setup

Install [uv](https://docs.astral.sh/uv/), then:

```sh
uv sync --group dev
uv run pytest --cov                 # unit and replay tests, offline
uv run ruff check --fix . && uv run ruff format . && uv run mypy
```

## Generated code

`digikey/v4/` is generated from `openapi/specs/` and must not be edited by hand. To regenerate (Java 11+
needed):

```sh
python openapi/generate.py          # from the committed specs
python openapi/generate.py --fetch  # download the latest specs from DigiKey first
```

To support another DigiKey API, follow [openapi/README.md](openapi/README.md#adding-a-digikey-api).

## Tests

* `tests/unit`: the hand-written code, with a fake HTTP layer below the generated clients. Most changes
  only need these.
* `tests/replay`: real responses recorded with [vcrpy](https://vcrpy.readthedocs.io/) and replayed
  offline. They prove the generated models parse what DigiKey actually returns. To (re)record you need a
  production app and a sandbox app:

  ```sh
  export DIGIKEY_PROD_CLIENT_ID=... DIGIKEY_PROD_CLIENT_SECRET=...
  export DIGIKEY_SANDBOX_CLIENT_ID=... DIGIKEY_SANDBOX_CLIENT_SECRET=...
  uv run pytest tests/replay --record-mode=rewrite
  ```

  Tokens, client ids and secrets are scrubbed automatically. Review the cassette diff before committing:
  it must not contain credentials or personal data.
* `tests/live`: smoke tests against the real API, run weekly by CI. Locally:
  `DIGIKEY_LIVE=1 uv run pytest -m live` with the variables above.

## Releasing (maintainer)

1. Move the "Unreleased" entries in `CHANGELOG.md` under a new version heading and merge to `master`.
2. Tag and push: `git tag v2.1.0 && git push origin v2.1.0`. The release workflow builds, publishes to
   PyPI with Trusted Publishing and creates the GitHub release. Tags like `v2.1.0rc1` are pre-releases.

Dependency updates arrive as Dependabot PRs and merge themselves when CI passes (minor and patch only).
