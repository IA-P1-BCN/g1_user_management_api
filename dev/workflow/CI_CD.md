# CI/CD & Quality Gates

GitHub Actions workflows under `.github/workflows/`. Branch protection (`docs/dev/git/CONVENTIONS.md`) requires these checks before merge.

## PR pipeline (`ci.yml`)

Runs on every pull request; `concurrency` cancels superseded runs.

1. **Lint & format** — `ruff check . && ruff format --check .`
2. **Type-check** — `mypy app` (strictness grows over time; no new untyped code)
3. **Tests** — `pytest --cov=app --cov-fail-under=80`; integration tests get a disposable Postgres service container; migrations run against it (`docs/dev/database/CONVENTIONS.md`)
4. **Dependency audit** — `pip-audit` (security, `docs/dev/backend/CONVENTIONS.md`)
5. **Spec validation** — `openspec validate` (`docs/dev/workflow/CONVENTIONS.md`)
6. **OpenAPI contract check** — `spectral lint api/openapi.yaml`; then diff FastAPI's exported schema against the committed spec with `oasdiff` — fail on drift or breaking changes (`docs/dev/backend/fastapi/CONVENTIONS.md`)
7. **Build image** — proves the Dockerfile builds (`docs/dev/deployment/docker/CONVENTIONS.md`); not pushed

Dependencies are installed with **uv** from the committed `uv.lock` (`astral-sh/setup-uv` with cache). Pipeline steps call **Taskfile** targets (`task lint`, `task test`, …) wherever they exist, so CI and local machines run exactly the same commands.

## Merge pipeline

On merge to `main`:

1. **Changelog** workflow regenerates `CHANGELOG.md` (see `docs/dev/git/CONVENTIONS.md`).
2. **Deploy** workflow builds and pushes `ghcr.io/<org>/<app>:<git-sha>`, then deploys to the target environment using GitHub **environment secrets** (never repo-level secrets for prod).

## Local hooks

`.pre-commit-config.yaml` mirrors CI (`ruff`, `ruff format`, basic hygiene) so failures happen before the push, not after. `pre-commit install` is part of project setup.

## Gate summary

| Gate | Threshold |
|---|---|
| ruff | zero findings |
| mypy | zero new errors |
| pytest | all green, coverage ≥ 80% |
| pip-audit | no known CVEs in direct deps |
| openspec validate | valid structure |
| spectral | zero spec findings |
| oasdiff | exported schema == committed spec, no breaking changes |
