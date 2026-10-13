# FastAPI Conventions

**Canonical reference: [`docs/prompts/FASTAPI_BESTPRACTICES.md`](../../../prompts/FASTAPI_BESTPRACTICES.md)** — read it before writing any FastAPI code. The `fastapi` agent skill (see `skills-lock.json`) also applies automatically when working on this repo.

## OpenAPI is the single source of truth

Following [OpenAPI as the Single Source of Truth](https://medium.com/@razvandubau/openapi-as-the-single-source-of-truth-fe5f2185b430): the **contract is designed first, agreed, and committed** — everything else is generated or verified from it. Alignment before implementation.

1. **Spec-first** — new/changed endpoints are designed in the committed spec `api/openapi.yaml` **before** implementation. Spec changes are reviewed like code (PR) and land with the story that needs them; acceptance criteria reference spec paths, not code files.
2. **Swagger always on** — FastAPI serves Swagger UI at `/docs` and ReDoc at `/redoc` from the contract, in every environment. The docs are the API's face; never disable them.
3. **Generate, don't hand-write** — clients, DTOs, docs sites, and mock servers are generated from the spec (openapi-generator / Redocly CLI). Consumers (frontend, mobile, QA) develop against generated mocks in parallel with the backend — never against hand-written clients.
4. **Versioned contract** — the spec carries a semver version; breaking changes bump the major and go through `/v2` path versioning, not silent edits. Generated artifacts are pinned to the spec version they came from.
5. **Validation mirrors the spec** — `required`, `min/max`, `pattern`, `enum` in the spec must be enforced at runtime by the matching Pydantic models (see below); the CI contract check guarantees the two cannot drift.
6. **Contract testing in CI** — the OpenAPI schema FastAPI exports must **match the committed spec**: the PR pipeline diffs them (oasdiff) and fails on any breaking change or drift (`docs/dev/workflow/CI_CD.md`).

The known cost is discipline: the spec must be updated in the same PR as the behaviour change, or CI fails — that failure is the point.

## Project rules

- **App layout**: routers per domain under `app/<domain>/router.py` with models/schemas/services beside them; `app/main.py` only wires routers, lifespan, and middleware.
- **Pydantic v2** for request/response schemas; response models are always explicit (`response_model=`) so the exported schema stays equal to the contract.
- **`async` everywhere** on the request path; anything blocking (sync DB drivers, file hashing) goes to a threadpool (`run_in_executor` / `def` endpoint).
- **Dependencies** carry auth, DB sessions, and pagination — routers never open sessions themselves.
- **Lifespan** (not deprecated `on_event`) for startup/shutdown: DB engine, clients, instrumentation.
- Errors use typed exception handlers that emit the error schema declared in the spec.
- Every endpoint lands with its tests (TDD, `../CONVENTIONS.md`) and appears in the OpenAPI docs with tags matching its domain.
