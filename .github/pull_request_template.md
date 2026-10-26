## What and why

## Checklist
- [ ] Tests added or updated; `uv run pytest --cov` passes
- [ ] `uv run ruff check . && uv run ruff format --check . && uv run mypy` pass
- [ ] `digikey/v4/` only changed by running `python openapi/generate.py`
- [ ] CHANGELOG.md entry under "Unreleased" for user-visible changes
- [ ] No credentials, tokens or personal data in code, logs or cassettes
