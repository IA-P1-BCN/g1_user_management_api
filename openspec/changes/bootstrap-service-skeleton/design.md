# Design

## Context

Ver `proposal.md` — Why. El repositorio está vacío; este change crea el esqueleto sobre el que crecerán todas las historias. Restricciones vigentes de `docs/dev/`: uv como único gestor de paquetes, Taskfile como única entrada, ruff (E/W/B, línea 100), settings con pydantic-settings validados al arranque, logging JSON, `/health` + `/ready`, contrato spec-first en `api/openapi.yaml` y layout `src/` (fijado en AGENTS.md).

## Goals / Non-Goals

**Goals**

- Arrancar el servicio con `task dev` y verificarlo con `curl /health`
- Que cada historia posterior solo añada su dominio bajo `src/<domain>/`
- Tests sin base de datos real (dependencias sobreescribibles)

**Non-Goals**

- Modelos y migraciones (Alembic llega con la historia #12); autenticación (#2/#3)
- Contenedores (#24) y CI completa con cobertura/pip-audit (#21) — aquí solo ruff + pytest
- Métricas Prometheus (fase posterior)

## Decisions

1. **App factory + lifespan** (nunca `on_event`): `create_app()` monta routers y middleware; el lifespan crea y dispose el engine. Alternativa descartada: módulo con app global — peor testabilidad.
2. **`/health` sin BD; `/ready` con chequeo `SELECT 1` inyectado como dependencia**: los tests sobreescriben la dependencia y no necesitan Postgres. Un solo engine por proceso con `pool_pre_ping` (BESTPRACTICES).
3. **Logging con stdlib + JSONFormatter propio** (sin structlog): cero dependencias extra; un middleware añade request id (uuid4), ruta, estado y duración. structlog se puede adoptar más adelante sin cambiar el contrato del spec.
4. **Un único `Settings` global en `src/config.py`**: con un solo dominio todavía, el Settings global es el mínimo viable; se dividirá por dominio cuando existan dominios.
5. **`SECRET_KEY` y `DATABASE_URL` requeridas, conexión lazy**: el arranque falla rápido si faltan (spec), pero no se conecta a la BD al importar — el engine es perezoso, `/ready` detecta la caída con 503.
6. **`api/openapi.yaml` mínimo con `/health` y `/ready`**: spec-first desde el primer día; el chequeo automático de drift (spectral + oasdiff) llega con la CI completa (#21).
7. **CI mínima de un solo job**: `uv sync --locked` → `task lint` → `task test`. Cobertura ≥80% y pip-audit llegan con #21/#22.

## Risks / Trade-offs

- [Dos fuentes de contrato (yaml + código generado) pueden divergir] → por ahora revisión manual; #21 añade oasdiff en CI.
- [Python local 3.14 vs mínimo 3.11] → `.python-version` fija la versión del proyecto; uv instala el intérprete exacto y `uv.lock` lo pina.
- [Sin BD local el desarrollador no puede ver `/ready` en verde] → aceptado por ahora; `DATABASE_URL` apunta a la BD que cada equipo tenga; docker-compose llega con #24.

## Migration Plan

Primera entrega del servicio — no hay despliegue previo que migrar. Rollback = revert del PR.

## Open Questions

Ninguna que bloquee: las decisiones aplazables están asignadas a historias concretas (#12 Alembic, #21 CI completa, #24 contenedores).
