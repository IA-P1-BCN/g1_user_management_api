# Tasks

## 1. Proyecto y tooling (sub-issue #31)

- [ ] 1.1 Inicializar el proyecto uv (`pyproject.toml`, `.python-version`, `uv.lock`) con las dependencias del proposal y verificar que `uv sync --locked` instala el entorno
- [ ] 1.2 Crear `Taskfile.yml` con `install`/`dev`/`test`/`lint` y verificar que `task lint` y `task test` se ejecutan
- [ ] 1.3 Configurar ruff en `pyproject.toml` (reglas E/W/B, línea 100, formato) y verificar `task lint` en verde sobre el código existente

## 2. Aplicación FastAPI (sub-issue #32; config de #33)

- [ ] 2.1 Crear `src/config.py` (`Settings` de pydantic-settings: `SECRET_KEY` y `DATABASE_URL` requeridas, soporte `.env`) y verificar con test que el arranque falla rápido nombrando la variable ausente
- [ ] 2.2 Crear `src/logging_config.py` (formatter JSON) y el middleware de petición (request id, ruta, estado, duración) y verificar con test que el log de una petición es JSON parseable con esos campos
- [ ] 2.3 Crear `src/main.py` (`create_app` + lifespan) y `src/health/router.py` con `GET /health` y `GET /ready` (chequeo de BD como dependencia sobreescribible) y verificar con tests: `/health` 200 sin BD, `/ready` 200 con BD stub, `/ready` 503 con BD caída
- [ ] 2.4 Verificar con tests que `/docs` y `/redoc` responden 200

## 3. Base de datos y contrato (sub-issue #33)

- [ ] 3.1 Crear `src/database.py` (engine async con `pool_pre_ping`, `async_sessionmaker`, `get_db`) y verificar con test que `get_db` entrega una sesión (stub) y la cierra
- [ ] 3.2 Crear `api/openapi.yaml` con `/health` y `/ready` (spec-first) y verificar que el YAML parsea y describe ambos endpoints

## 4. CI y entrega (sub-issue #34)

- [ ] 4.1 Crear `.env.example` (SECRET_KEY, DATABASE_URL) y asegurar `.env` en `.gitignore`; verificar que `git status` no muestra `.env`
- [ ] 4.2 Crear `.github/workflows/ci.yml` (uv sync --locked → `task lint` → `task test` en cada PR) y verificar que el YAML parsea
- [ ] 4.3 Crear `.pre-commit-config.yaml` (ruff) y verificar `uv run pre-commit run --all-files` en verde

## 5. Integración final

- [ ] 5.1 Ejecutar `task lint` + `task test` en verde y `openspec validate bootstrap-service-skeleton` sin errores
- [ ] 5.2 Arrancar `task dev` y verificar manualmente `/health`, `/ready`, `/docs`, `/redoc`; registrar el resultado en la PR

## Workflow follow-up

- Revisión humana de la PR y merge (squash) — regla del repo: 1 aprobación
- `openspec archive bootstrap-service-skeleton` tras el merge (fusiona los deltas en `openspec/specs/`)
- Cerrar los sub-issues #31–#34 y la historia #1
