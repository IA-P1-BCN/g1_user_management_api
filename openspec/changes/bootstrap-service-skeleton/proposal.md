# Proposal

**Refs #1** — historia "Como equipo, quiero un esqueleto runnable del servicio".

## Why

El repositorio está vacío: no hay código, ni herramienta de construcción, ni CI. Toda historia posterior (registro, login, CRUD) necesita una base ejecutable sobre la que construir. Esta primera historia crea ese esqueleto.

## What Changes

- Proyecto gestionado con **uv** (`uv.lock` commiteado) y **Taskfile** como único punto de entrada (`task install`, `task dev`, `task test`, `task lint`)
- Aplicación **FastAPI** con `GET /health` (liveness) y `GET /ready` (readiness con chequeo de BD)
- Documentación interactiva siempre activa: Swagger UI en `/docs` y ReDoc en `/redoc`
- Configuración por entorno con **pydantic-settings** (`SECRET_KEY`, `DATABASE_URL`), validada una vez al arranque; `.env` git-ignored
- Motor **SQLAlchemy 2.0 async** a PostgreSQL con fábrica de sesiones — sin modelos todavía (llegan con la historia #2)
- **Logging JSON** estructurado (request id, ruta, estado, duración)
- CI mínima en GitHub Actions: ruff + pytest en cada PR
- `openspec` inicializado en el repositorio

## Capabilities

### New Capabilities

- `service-health`: endpoints de liveness (`/health`) y readiness (`/ready`) que indican si el servicio está vivo y operativo
- `api-docs`: documentación interactiva de la API siempre disponible en todos los entornos
- `app-configuration`: configuración por entorno, validada al arranque, sin secretos en código ni logs
- `observability`: logging estructurado JSON con metadatos de cada petición

### Modified Capabilities

(ninguna — es la primera historia del proyecto)

## Impact

- Nuevo: `src/` (main, config, database, logging_config, health/), `tests/`, `Taskfile.yml`, `pyproject.toml`, `uv.lock`, `api/openapi.yaml`, `.github/workflows/ci.yml`, `.pre-commit-config.yaml`, `.env.example`
- Sin breaking changes: no existe comportamiento previo
- Dependencias nuevas: fastapi ≥0.115, uvicorn, pydantic ≥2.7, pydantic-settings ≥2.4, sqlalchemy ≥2.0, asyncpg; desarrollo: pytest, pytest-asyncio, httpx ≥0.27, ruff ≥0.6
