# Backend Standards

Python backend conventions. FastAPI-specific rules live in [`fastapi/`](./fastapi/CONVENTIONS.md); this file covers everything else.

## TDD

Red → green → refactor. No exceptions for `feat` or `fix` work.

1. **Red**: write one failing test that expresses the next small slice of behaviour (ideally an acceptance criterion from the story — see `docs/dev/workflow/CONVENTIONS.md`).
2. **Green**: write the **minimum** production code to pass it. Fake it, return a constant, triangulate.
3. **Refactor**: clean up test and production code while staying green, then commit.

Rules:

- No production code without a failing test that demanded it. Refactors under green don't need new tests.
- One logical assertion per test; test names describe behaviour: `test_refresh_token_rotation_invalidates_old_token`.
- Tests are deterministic: freeze time, fake external services (httpx `MockTransport`, `pytest` fixtures), never hit real networks or the real DB in unit tests. Integration tests get a disposable DB (testcontainers or a compose service).
- Every acceptance criterion in a story maps to at least one test before the story leaves `Testing`.
- PRs for `feat`/`fix` without tests are rejected (enforced at review, `docs/dev/git/CONVENTIONS.md`).

## Style: PEP 8, enforced by ruff

PEP 8 is the baseline; [ruff](https://docs.astral.sh/ruff/) enforces it and formats the code. Config lives in `pyproject.toml`.

- `ruff check` (pycodestyle `E`/`W` rules + bugbear `B`) and `ruff format` (black-compatible); line length 100.
- Naming: `snake_case` functions/variables, `PascalCase` classes, `UPPER_CASE` constants, `_leading_underscore` for internal.
- Type hints required on all public functions; docstrings on public modules/classes/functions.
- Imports sorted by ruff (`isort` rules); no `import *` anywhere.
- Lint and format run in CI and pre-commit (see `docs/dev/workflow/CI_CD.md`); a PR that fails ruff does not get reviewed.

## Configuration & secrets

Twelve-factor: all configuration comes from the environment.

- One `Settings(BaseSettings)` class via `pydantic-settings`, validated once at startup — fail fast on anything missing.
- `.env` files are local-only and git-ignored; secrets are never committed, never logged, never baked into images.
- Environments (dev/staging/prod) differ **only** by environment variables.
- Secrets in CI/CD come from GitHub environment secrets, never from the repo.

## Security

- Validate **all** input with Pydantic models; never trust raw request data.
- AuthN/AuthZ at the router-dependency level; deny by default on new routers.
- Parameterized queries only (SQLAlchemy) — string-built SQL is rejected in review.
- Rate limiting on auth and expensive endpoints; CORS restricted to explicit origins.
- `pip-audit` runs in CI; vulnerable dependencies block the merge.

## Observability

- Structured JSON logs (request ID, route, status, duration); no PII or secrets in logs.
- `/health` (liveness) and `/ready` (readiness, checks DB) endpoints for orchestration.
- Prometheus metrics via `prometheus-fastapi-instrumentator`; alert on error rate and latency, not just uptime.
