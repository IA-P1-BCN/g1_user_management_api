# Docker Conventions

Rules for the service image and local development stack.

- **Multi-stage build**: a `builder` stage installs dependencies, a slim final stage (`python:3.x-slim`) copies only what runs. No compilers, no caches in the final image.
- **Dependencies are pinned** via **uv** from the committed `uv.lock` (`uv sync --frozen` in the builder stage), never `latest` tags.
- **Non-root user** (`USER app`); the container has no sudo and writes nothing outside `/tmp` and its workdir.
- **`HEALTHCHECK`** hits `/health` (see observability, `docs/dev/backend/CONVENTIONS.md`) so orchestrators can act on real health.
- **`.dockerignore`** excludes `.git`, `venv`, `__pycache__`, `tests/`, `.env`, docs — the image stays small and secrets stay out.
- **No secrets in image layers**: config arrives as environment variables at runtime (twelve-factor, `docs/dev/backend/CONVENTIONS.md`).
- **Tags are immutable**: `ghcr.io/<org>/<app>:<git-sha>` for deploys; `latest` is never deployed.
- **Local development** uses `docker compose` for infrastructure (Postgres, anything stateful); the app itself runs natively with hot reload.
- Images are built in CI on every PR (proves buildability) and on `main` for deploys — see `docs/dev/workflow/CI_CD.md`.
