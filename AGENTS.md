# testme

**User Management API** — a centralized FastAPI service with JWT auth and interactive OpenAPI docs, built agentically: AI agents write the code, the human team defines, reviews, and merges.

**Objective** (from [`docs/business/CLIENT_SPECS.md`](docs/business/CLIENT_SPECS.md)):

> Desarrollar una API REST con **FastAPI** que permita gestionar usuarios (alta, consulta, edición y baja) con **autenticación basada en JWT** y **documentación interactiva con Swagger (OpenAPI)**, de forma que cualquier equipo pueda integrarse con ella sin necesidad de leer el código.

This file is an **index only** — each section maps to a folder under `docs/`; open the linked doc for the rules that apply to your task (progressive disclosure). Doc zones: `docs/business/` (project + client), `docs/dev/` (engineering conventions), `docs/prompts/` (reusable prompts).

## Folder Structure
├── src/
│   ├── main.py            # FastAPI app + lifespan
│   ├── config.py          # Settings (pydantic-settings)
│   ├── database.py        # async engine + session factory + get_db
│   ├── logging_config.py  # JSON logging
│   └── <domain>/          # router.py · schemas.py · models.py · service.py
├── api/
│   └── openapi.yaml       # spec-first contract
├── openspec/              # living spec: changes/ (proposals) + specs/ (archived)
├── tests/
├── Taskfile.yml · pyproject.toml · uv.lock
└── README.md

## Working rules

From the client spec — non-negotiable:

- One Kanban task = one agent session = one branch = one PR; **human review before merge**
- **Tests are the contract**: leave tests passing; fix code, never delete tests
- **Specs before code** (SDD, OpenSpec): no implementation before the spec change is approved
- **Vertical slices**: every story delivers thin end-to-end functionality (endpoint → service → repository → model → tests) that can ship, test, and demo on its own — never horizontal "layer" stories

## Stack

- Python ≥ 3.11 · FastAPI ≥ 0.115 · Pydantic ≥ 2.7 (+ pydantic-settings)
- PostgreSQL + SQLAlchemy 2.0 (async) + Alembic — spec says "SQL DB + ORM"; Postgres is the working assumption (`docs/dev/database/CONVENTIONS.md`)
- Auth: OAuth2 Password Flow + JWT via **PyJWT** (not python-jose); bcrypt/argon2 password hashing
- Contract: OpenAPI 3.1 **spec-first** (`api/openapi.yaml`); Swagger UI `/docs` + ReDoc `/redoc` always on
- Testing: pytest + httpx AsyncClient; coverage ≥ 80%
- **uv** — the only package/venv manager; `uv.lock` is committed, dependencies pinned
- **Taskfile** (go-task) — `task` is the single entry point (`task install`, `task dev`, `task test`, `task lint`, `task migrate`…); run `task <cmd>` instead of raw commands whenever the task exists
- Quality: ruff (lint + format), mypy, pre-commit, pip-audit
- CI/CD: GitHub Actions, git-cliff changelog, Docker multi-stage images
- Canonical version matrix: `docs/prompts/FASTAPI_BESTPRACTICES.md`

## Skills in use

Managed by `skills-lock.json` (installed under `.zcode/skills/` and `.agents/skills/`):

- **fastapi** — its conventions apply to all backend code (see `docs/dev/backend/fastapi/CONVENTIONS.md`)
- **setup-matt-pocock-skills** (engineering suite) — reads the `## Agent skills` section below

## Agent skills

### Issue tracker

Issues are tracked as GitHub issues in this repo, via the `gh` CLI. See `docs/dev/agents/issue-tracker.md`.

### Domain docs

Single-context: one `GLOSSARY.md` and `docs/adr/` at the repo root. See `docs/dev/agents/domain.md`.

## Business

- `docs/business/CLIENT_SPECS.md` — the client contract: requirements by level (esencial → experto), stakeholders, working rules
- `docs/business/CLIENT_DEMO_RULES.md` — demo-day presentation structure

## Git

See `docs/dev/git/CONVENTIONS.md`.

- **Conventional Commits v1.0** are mandatory (`feat`/`fix`/`perf`/… — the changelog parses them)
- **Conventional branches**: `<type>/<story-number>-<slug>` (e.g. `feat/1-bootstrap-service-skeleton`, `fix/12-alembic-migrations`); one branch per story = one PR
- `main` is protected: PR + **1 approval**, no direct pushes
- `CHANGELOG.md` is auto-generated on merge to `main` (git-cliff) — never hand-edit it

## Backend

See `docs/dev/backend/CONVENTIONS.md`; FastAPI specifics in `docs/dev/backend/fastapi/CONVENTIONS.md`.

- **OpenAPI is the single source of truth** (spec-first in `api/openapi.yaml`; clients/mocks generated; contract check in CI; Swagger UI always on)
- **TDD**: red → green → refactor; no production code without a failing test
- **PEP 8** enforced by ruff; type hints on public functions
- Config and secrets from the environment only (pydantic-settings); JSON logs + `/health` + metrics

## Database

See `docs/dev/database/CONVENTIONS.md` — Alembic migrations only, no manual DDL; every FK indexed.

## Deployment

See `docs/dev/deployment/docker/CONVENTIONS.md` — multi-stage, non-root, healthchecked images; tags are git SHAs, `latest` is never deployed.

## Workflow

See `docs/dev/workflow/CONVENTIONS.md` and `docs/dev/workflow/CI_CD.md`.

- **SDD with OpenSpec**: no implementation before the spec change is approved; **one story = one `openspec/changes/<id>/` folder**; the spec is the behavioral source of truth — if board and spec disagree, trust the spec
- **GitHub Project board** (Scrum): epic → milestone, story → `story` label, subtask → `task` label (only independently shippable pieces); columns Backlog / Sprint Backlog / In Review / Testing / Blocked / Ready for Deployment / Hell / Done; stories carry concise ACs + a spec link, never full Given/When/Then detail
- CI gates on every PR: ruff, mypy, pytest ≥ 80% coverage, pip-audit, openspec validate, OpenAPI contract check (spectral + oasdiff)

## Prompts

- `docs/prompts/FASTAPI_BESTPRACTICES.md` — canonical FastAPI reference (versions, structure, Do/Don't)
- `docs/prompts/AGENTS_FIXER.md` — prompt for refactoring this file
