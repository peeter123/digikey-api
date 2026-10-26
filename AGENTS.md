# Working on digikey-api

Rules for anyone changing this repository, human or AI agent. CI enforces most of them.

## Layout

- `digikey/v4/**` is **generated** from `openapi/specs/*.json` by `openapi/generate.py`. Never edit it by
  hand: change the spec handling or generator settings and regenerate. CI fails on any hand edit.
- Everything else in `digikey/` is the small hand-written layer: `client.py` (DigikeyClient), `oauth/`
  (token providers), `exceptions.py`, `__init__.py` (1.x compatibility functions). Keep it small.
- `tests/unit` (offline, fakes below urllib3), `tests/replay` (recorded cassettes), `tests/live`
  (real API, opt-in).

## Rules

1. Every change to hand-written code comes with tests. Coverage of hand-written code stays at 90% or more.
2. Pass parameters to generated methods **by keyword only**; their positional order follows the spec and
   is not stable.
3. Errors are raised (`DigikeyApiError` and friends), never logged and swallowed.
4. Secrets never appear in code, logs, fixtures or cassettes. Never log tokens. Cassettes are scrubbed by
   `tests/replay/conftest.py`; check the diff of every new cassette anyway. Never commit `.mcp.json`,
   `.env` or token storage files.
5. Public API changes follow semver and get an entry in `CHANGELOG.md` under "Unreleased".
6. Supported Python versions are exactly the CI matrix in `.github/workflows/ci.yml`.
7. New runtime dependencies need a good reason; prefer the standard library.
8. Ruff is the final gate, not a per-edit step: before you finish or commit, run
   `uv run ruff check --fix . && uv run ruff format .`, then make sure `uv run ruff check .`,
   `uv run ruff format --check .` and `uv run mypy` report nothing. The Claude Code Stop hook in
   `.claude/settings.json` blocks finishing while changed files fail ruff.

## Commands

```sh
uv sync --group dev                  # set up
uv run pytest --cov                  # unit + replay tests
uv run ruff check --fix . && uv run ruff format . && uv run mypy
python openapi/generate.py           # regenerate digikey/v4 (Java 11+)
```

## Adding a DigiKey API

See `openapi/README.md`: add the spec to `APIS` in `openapi/generate.py`, run `--fetch`, add wrapper
methods to `digikey/client.py`, add tests.
